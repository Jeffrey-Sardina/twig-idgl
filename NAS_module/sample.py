#!/usr/bin/env python3

# Adapted from https://automl.github.io/HpBandSter/build/html/auto_examples/example_1_local_sequential.html
# and https://automl.github.io/HpBandSter/build/html/quickstart.html

import random
import logging
import yaml
import argparse
import numpy
import torch
import os
import shutil
from hpbandster.optimizers import BOHB as BOHB
from hpbandster.core.worker import Worker
import hpbandster.core.nameserver as hpns
import hpbandster.core.result as hpres
import ConfigSpace as CS #hpbandster supports float, int, and categorial hyperparameters only, not all in CS

import sys
sys.path.append("/workspace/") #Needed to be able to import from GNN_module
sys.path.append("/workspace/GNN_module/src/") #Needed to allow imported in code in GNN_module
from GNN_module.src.main import main as GNN_run

import logging
logging.basicConfig(level=logging.WARNING)

hyperparams_to_override = set()

class GNN_Worker(Worker):
    '''
    A class to define the GNN we want to run and allow it be used with BOHB
    '''
    def __init__(self, idgl_config_file, *args, twig_config=None, **kwargs):
        '''
        Set up the worker's configuration
        '''
        super().__init__(*args, **kwargs)

        self.run_id = kwargs["run_id"]
        self.twig_config = twig_config

        # Load base IDGL file
        with open(idgl_config_file, "r") as conf:
            self.idgl_conf = yaml.load(conf, Loader=yaml.FullLoader)

        # Load override parameters from the TwigJob file
        if "idgl_params" in self.twig_config and self.twig_config["idgl_params"]:
            for param in self.twig_config["idgl_params"]:
                self.idgl_conf[param] = self.twig_config["idgl_params"][param]
                print(param, self.twig_config["idgl_params"][param])
                print(self.idgl_conf[param])

    def compute(self, config_id, config, budget, working_directory):
        """
        Parameters:
            config_id: (int tuple) an int tuple uniquely identiying this run provided by HyperBandster
            config: (dict) dictionary containing the sampled configurations by the optimizer
            budget: (float) amount of epochs to use
            working_directory: (str) the current working directory

        Returns:
            dictionary with mandatory fields:
                'loss' (scalar)
                'info' (dict)

        IDGL normally loads config from a YAML file, but I can just pass it a dictionary with the same struct
        The parameters of this dict need to be loaded into the full idgl_conf needed by IDGL. Then, the resultant
            config can be used to call IDGL's main function
        """

        # Load checkpointing data
        checkpoint_dir = os.path.join(self.twig_config["out_dir"], self.run_id, "_".join(str(x) for x in config_id))
        checkpoint_file = os.path.join(checkpoint_dir, "checkpoint.yml")

        # Restore checkpoint if it exists; else create a checkpoint directory
        if os.path.isdir(checkpoint_dir):
            if os.path.exists(checkpoint_file):
                try:
                    with open(checkpoint_file, 'r') as checkpoint:
                        checkpoint_data = yaml.load(checkpoint, Loader=yaml.FullLoader)
                    print("Using checkpoint for iteration with config_id:", config_id)
                    print(os.path.abspath(checkpoint_file))
                    return {
                        'loss': checkpoint_data["loss"], # this is the a mandatory field to run hyperband
                        'info': checkpoint_data["info"] # can be used for any user-defined information - also mandatory
                    }
                except:
                    raise ValueError("Could not load checkpoint.", checkpoint_file)
            else:
                    shutil.rmtree(checkpoint_dir)
        
        # Load the correct model configuration
        tmp_idgl_conf = {k:self.idgl_conf[k] for k in self.idgl_conf}
        for hyperparam in hyperparams_to_override:
            tmp_idgl_conf[hyperparam] = config[hyperparam]
        tmp_idgl_conf['max_epochs'] = budget
        tmp_idgl_conf['out_dir'] = checkpoint_dir #"/tmp/" + "iteration_id_" + str(random.random())

        # Run the model configuration and collect the results
        res = GNN_run(tmp_idgl_conf)

        # Release CUDA memory
        torch.cuda.empty_cache() #Otherwise old runs might take up memory later runs could use

        # Get Run Data
        return_dict = {
                    'loss': float(res),  # this is the a mandatory field to run hyperband
                    'info': checkpoint_file #res  # can be used for any user-defined information - also mandatory
                }

        # Write the results to disk as a checkpoint
        with open(checkpoint_file, 'w') as checkpoint:
            yaml.dump(return_dict, checkpoint)

        return return_dict
    
    @staticmethod
    def get_configspace(twig_config):
        '''
        Define the hyperparameter space to be searched
        '''
        config_space = CS.ConfigurationSpace()

        for hyperparam in twig_config["hyperparameters"]:
            hyperparams_to_override.add(hyperparam)
            hyperparam_data = twig_config["hyperparameters"][hyperparam]
            print(hyperparam_data)
            if hyperparam_data['type'] == "uniform_float":
                print("uniform_float")
                config_space.add_hyperparameter(CS.UniformFloatHyperparameter(hyperparam, lower=hyperparam_data["min"], upper=hyperparam_data["max"]))
            elif hyperparam_data['type'] == "uniform_integer":
                print("uniform_integer")
                config_space.add_hyperparameter(CS.UniformIntegerHyperparameter(hyperparam, lower=hyperparam_data["min"], upper=hyperparam_data["max"]))
            elif hyperparam_data['type'] == "log_uniform_float":
                print("log_uniform_float")
                config_space.add_hyperparameter(CS.UniformFloatHyperparameter(hyperparam, lower=hyperparam_data["min"], upper=hyperparam_data["max"], log=True))
            elif hyperparam_data['type'] == "log_uniform_integer":
                print("log_uniform_integer")
                config_space.add_hyperparameter(CS.UniformIntegerHyperparameter(hyperparam, lower=hyperparam_data["min"], upper=hyperparam_data["max"], log=True))
            else:
                raise ValueError("Unrecognized hyperparam type: ", hyperparam['type'])
        return config_space

def run_sampler(args):
    '''
    Run the Neural Architecture Search (based on a BOHB sampler)
    '''
    # Configure Logger
    log_dir = os.path.join(args["bohb_log_dir"], args['run_id'])
    result_logger = hpres.json_result_logger(directory=log_dir, overwrite=args["allow_resume"])

    # Step 1: Start a nameserver
    # Every run needs a nameserver. It could be a 'static' server with a
    # permanent address, but here it will be started for the local machine with the default port.
    # The nameserver manages the concurrent running workers across all possible threads or clusternodes.
    # Note the run_id argument. This uniquely identifies a run of any HpBandSter optimizer.
    NS = hpns.NameServer(run_id=args["run_id"], host=args["host_addr"], working_directory=os.path.join(args["out_dir"], args["run_id"]), port=None)
    NS.start()

    # Step 2: Start a worker
    # Now we can instantiate a worker, providing the mandatory information
    # Besides the sleep_interval, we need to define the nameserver information and
    # the same run_id as above. After that, we can start the worker in the background,
    # where it will wait for incoming configurations to evaluate.
    worker = GNN_Worker(args["idgl_config_file"],
        nameserver=args["host_addr"],
        run_id=args["run_id"],
        twig_config=args)
    worker.run(background=True)

    # Step 3: Run an optimizer
    # Now we can create an optimizer object and start the run.
    # Here, we run BOHB, but that is not essential.
    # The run method will return the `Result` that contains all runs performed.
    bohb = BOHB(configspace = worker.get_configspace(args),
                run_id = args["run_id"],
                nameserver=args["host_addr"],
                min_budget=args["min_budget"],
                max_budget=args["max_budget"],
                result_logger=result_logger
            )
    res = bohb.run(n_iterations=args["n_iterations"])

    # Step 4: Shutdown
    # After the optimizer run, we must shutdown the master and the nameserver.
    bohb.shutdown(shutdown_workers=True)
    NS.shutdown()

    # Step 5: Analysis
    # Each optimizer returns a hpbandster.core.result.Result object.
    # It holds informations about the optimization run like the incumbent (=best) configuration.
    # For further details about the Result object, see its documentation.
    # Here we simply print out the best config and some statistics about the performed runs.
    print("=========================")
    id2config = res.get_id2config_mapping()
    incumbent = res.get_incumbent_id()
    print('Best found configuration:', id2config[incumbent]['config'])
    print('A total of %i unique configurations where sampled.' % len(id2config.keys()))
    print('A total of %i runs where executed.' % len(res.get_all_runs()))
    print('Total budget corresponds to %.1f full function evaluations.'%(sum([r.budget for r in res.get_all_runs()])/args["max_budget"]))

    # Get the entire config used
    opt_config = id2config[incumbent]['config']
    with open(args["idgl_config_file"], "r") as conf:
        total_config = yaml.load(conf, Loader=yaml.FullLoader)
    for hyperparam in hyperparams_to_override:
        total_config[hyperparam] = opt_config[hyperparam]
    return total_config

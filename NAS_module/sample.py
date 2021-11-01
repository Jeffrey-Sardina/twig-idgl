#!/usr/bin/env python3

# Adapted from https://automl.github.io/HpBandSter/build/html/auto_examples/example_1_local_sequential.html
# and https://automl.github.io/HpBandSter/build/html/quickstart.html

import random
import logging
import yaml
import argparse
import numpy
from hpbandster.optimizers import BOHB as BOHB
from hpbandster.core.worker import Worker
import hpbandster.core.nameserver as hpns
import hpbandster.core.result as hpres
import ConfigSpace as CS #hpbandster supports float, int, and categorial hyperparameters

import sys
sys.path.append("/workspace/") #Needed to be able to import from GNN_module
sys.path.append("/workspace/GNN_module/src/") #Needed to allow imported in code in GNN_module
from GNN_module.src.main import main as GNN_run

class GNN_Worker(Worker):
    def __init__(self, idgl_config_file, additional_configs, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(idgl_config_file, "r") as conf:
            self.idgl_conf = yaml.load(conf)
        if additional_configs:
            for key in additional_configs:
                self.idgl_conf[key] = additional_configs[key]

    def compute(self, config, budget, **kwargs):
        """
        Parameters:
            config: dictionary containing the sampled configurations by the optimizer
            budget: (float) amount of epochs to use

        Returns:
            dictionary with mandatory fields:
                'loss' (scalar)
                'info' (dict)

        IDGL normally loads config from a YAML file, but I cna just pass it a dictionary with the same struct
        The parameters of this dict need to be loaded into the full idgl_conf needed by IDGL. Then, the resultant
            config can be used to call IDGL's main function
        """

        # Load the correct model configuration
        idgl_hyperparams = ['learning_rate'] #Should have the same name in both dictionaries
        for hyperparam in idgl_hyperparams:
            self.idgl_conf[hyperparam] = config[hyperparam]
        self.idgl_conf['max_epochs'] = budget
        self.idgl_conf['out_dir'] = "/tmp/" + "iteration_id_" + str(random.random())

        # Run the model configuration and collect the results
        res = GNN_run(self.idgl_conf)

        return {
                    'loss': float(res),  # this is the a mandatory field to run hyperband
                    'info': res  # can be used for any user-defined information - also mandatory
                }
    
    @staticmethod
    def get_configspace():
        config_space = CS.ConfigurationSpace()
        config_space.add_hyperparameter(CS.UniformFloatHyperparameter('learning_rate', lower=0, upper=10))
        return config_space

def run_sampler(args):
    # Configure Logger
    #logging.basicConfig(level=logging.WARNING)

    # # Get cmd line arguments
    # parser = argparse.ArgumentParser(description='Example 1 - sequential and local execution.')
    # parser.add_argument('--min_budget', type=float, help='Minimum budget used during the optimization.', default=9)
    # parser.add_argument('--max_budget', type=float, help='Maximum budget used during the optimization.', default=243)
    # parser.add_argument('--n_iterations', type=int, help='Number of iterations performed by the optimizer', default=4)
    # parser.add_argument('--run_id', type=str, help='Internal ID used to identify this run', default='nas_run_default_id')
    # parser.add_argument('--host_addr', type=str, help='Network address to host the internal data server', default='127.0.0.1')
    # parser.add_argument('--idgl_config_file', type=str, help='The configuration file for IDGL to use as a base')
    # args=parser.parse_args()


    # Step 1: Start a nameserver
    # Every run needs a nameserver. It could be a 'static' server with a
    # permanent address, but here it will be started for the local machine with the default port.
    # The nameserver manages the concurrent running workers across all possible threads or clusternodes.
    # Note the run_id argument. This uniquely identifies a run of any HpBandSter optimizer.
    NS = hpns.NameServer(run_id=args["run_id"], host=args["host_addr"], port=None)
    NS.start()

    # Step 2: Start a worker
    # Now we can instantiate a worker, providing the mandatory information
    # Besides the sleep_interval, we need to define the nameserver information and
    # the same run_id as above. After that, we can start the worker in the background,
    # where it will wait for incoming configurations to evaluate.
    GNN_Worker.iteration_id = 0
    worker = GNN_Worker(args["idgl_config_file"],
        additional_configs=args['idgl_params'][0],
        nameserver=args["host_addr"],
        run_id=args["run_id"])
    worker.run(background=True)

    # Step 3: Run an optimizer
    # Now we can create an optimizer object and start the run.
    # Here, we run BOHB, but that is not essential.
    # The run method will return the `Result` that contains all runs performed.
    bohb = BOHB(configspace = worker.get_configspace(),
                run_id = args["run_id"], nameserver=args["host_addr"],
                min_budget=args["min_budget"], max_budget=args["max_budget"]
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
    id2config = res.get_id2config_mapping()
    incumbent = res.get_incumbent_id()
    print('Best found configuration:', id2config[incumbent]['config'])
    print('A total of %i unique configurations where sampled.' % len(id2config.keys()))
    print('A total of %i runs where executed.' % len(res.get_all_runs()))
    print('Total budget corresponds to %.1f full function evaluations.'%(sum([r.budget for r in res.get_all_runs()])/args["max_budget"]))

#!/usr/bin/env python3

import yaml
import sys
import argparse
import os
import datetime
import hpbandster.core.result as hpres

import sys
sys.path.append("/workspace/")
from NAS_module.sample import run_sampler
from NAS_module.analyse import correlation_analysis
sys.path.append("/workspace/GNN_module/src/") #Needed to allow imported in code in GNN_module
from GNN_module.src.main import main as GNN_run

config = None

def in_idgl_dir(func):
    '''
    A decorator to run a certain function in a different directry.
    This is needed since IDGL needs to be run from its own directory, and
        writing the code with a decorate makes it a bit clearer
    '''
    def inner(*args, **kwargs):
        original_dir = os.getcwd()
        os.chdir(config["idgl_working_dir"]) # Avoid dir IDGL's dir errors in NAS and GNN functions
        output = func(*args, **kwargs)
        os.chdir(original_dir)
        return output
    return inner

def do_job():
    '''
    Run Neural Architecutre Search (NAS) to generate the neural net
    Then run IDGL on the resultant neural net and output results
    '''
    # Create AI
    # print('=========================NAS Starting=========================')
    # neural_architecture = neural_architecture_search()
    # print('=========================NAS Done=========================')
    # print('NA:', neural_architecture)

    # # Train AI
    # print('=========================Training Starting=========================')
    # accuracy = train_GNN(neural_architecture)
    # print('=========================Training Done=========================')
    # print('accuracy:', accuracy)

    # Run analysis
    print('=========================Analysis Starting=========================')
    accuracy = analyse()
    print('=========================Analysis Done=========================')

@in_idgl_dir
def neural_architecture_search():
    return run_sampler(config)

@in_idgl_dir
def train_GNN(neural_architecture):
    # Load some params, such as out dir, that are not part of NAS
    if "idgl_params" in config and config["idgl_params"]:
        for param in config["idgl_params"]:
            neural_architecture[param] = config["idgl_params"][param]
    neural_architecture["out_dir"] = config["out_dir"]
    return GNN_run(neural_architecture)

def analyse():
    correlation_analysis(config)

def load_config(filename):
    '''
    Load the config file from disk
    '''
    try:
        with open(filename, 'r') as config_file:
            config = yaml.load(config_file)
    except:
        raise ValueError("Could not load configuration for running Twig.", filename)
    return config

if __name__ == '__main__':
    print("Hello, I am Twig. I do my job!")

    # Some data for intelligent defaults
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    default_run_id = "twig_default_job_" + timestamp
    
    # Get input
    parser = argparse.ArgumentParser(description='Twig arguments')
    parser.add_argument('--do_your_job', type=str, help="YAML file speicifying Twig's job", default="TwigJob.yml")
    args=parser.parse_args()
    
    # Load job config
    print("Loading job details...", end='')
    config = load_config(args.do_your_job)
    print("success")

    #Run job
    print("Doing my job!")
    do_job()
    print("Job completed successfully!")
    exit(0)
    
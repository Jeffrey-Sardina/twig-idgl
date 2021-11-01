#!/usr/bin/env python3

import yaml
import sys
import glob
import argparse
import os

import sys
sys.path.append("/workspace/")
from NAS_module.sample import run_sampler

def do_job(config):
    os.chdir("/workspace/GNN_module/src/") #Avoid all the annoying dir errors
    run_sampler(config)

def load_config(filename):
    try:
        with open(filename, 'r') as config_file:
            config = yaml.load(config_file)
    except:
        raise ValueError("Could not load configuration for running Twig.", filename)
    
    return config

if __name__ == '__main__':
    print("Hello, I am Twig. I do my job!")

    #Get input
    parser = argparse.ArgumentParser(description='Twig arguments')
    parser.add_argument('--do_your_job', type=str, help="YAML file speicifying Twig's job", default="TwigJob.yml")
    args=parser.parse_args()
    
    # Load job config
    print("Loading job details...", end='')
    config = load_config(args.do_your_job)
    print("success")

    #Run job
    print("Doing my job!")
    do_job(config)
    print("Job completed successfully!")
    exit(0)
    
#!/usr/bin/env python3

import yaml
import argparse

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
    # Get input
    parser = argparse.ArgumentParser(description='Twig arguments')
    parser.add_argument('--yaml_file', type=str, help="YAML file speicifying Twig's job", default="TwigJob.yml")
    parser.add_argument('--item', type=str, help="Item whose value to retrive")
    args=parser.parse_args()
    
    # Load job config
    config = load_config(args.yaml_file)
    print(config[args.item])

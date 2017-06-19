"""
Copyright 2017 Pirate Hour Productions

Author: Alan Drees

Purpose: Implment a common accessor for the yaml configuration
"""

import yaml

config_filename = './config.yml'

def load_config():
    """
    Loads the configuration file in the current directory

    @param None

    @returns (dict) Dictionary of key/value pairs in the configuration
    """

    config = {}
    
    with open(config_filename, 'r') as configfile:
        config = yaml.load(configfile)

    return config


def validate_config():
    """
    Validate the configuration file

    @param None

    @returns (bool) true if valid, false otherwise
    """
    pass

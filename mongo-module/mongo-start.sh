#!/bin/bash

mongod --dbpath . --directoryperdb --journal --logpath log.log

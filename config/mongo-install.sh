#!/bin/bash

mongod --dbpath . --port 1234 --directoryperdb --journal --logpath log.log --nohttpinterface


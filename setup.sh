#!/bin/bash
conda create -n py39 python=3.9 -y
source activate py39
pip install -r requirements.txt

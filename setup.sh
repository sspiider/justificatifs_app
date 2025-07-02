#!/bin/bash
# Force Python 3.9 even if Cloud tries 3.13
conda create -n myenv python=3.9 -y
source activate myenv
pip install -r requirements.txt

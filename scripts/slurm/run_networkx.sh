#!/bin/bash

#SBATCH --job-name=networkx_test
#SBATCH --output=outputs/logs/networkx_%j.out
#SBATCH --error=outputs/logs/networkx_%j.err

#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

cd ~/earnings-call-analysis

source .venv/bin/activate

python scripts/graph/test_networkx.py
#!/bin/bash

#SBATCH --job-name=build_kg
#SBATCH --output=outputs/logs/build_kg_%j.out
#SBATCH --error=outputs/logs/build_kg_%j.err

#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G

cd ~/earnings-call-analysis

source .venv/bin/activate

python build_knowledge_graph.py
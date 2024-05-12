#!/bin/bash

#SBATCH --partition=mig_class
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=4:00:0
#SBATCH --job-name="icecot_test"
#SBATCH --output=slurm-%j.out
#SBATCH --mem=32G

module load anaconda
conda activate icecot # activate the Python environment
python src/test_model.py
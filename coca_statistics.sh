#!/bin/bash
#SBATCH --job-name=coca_statistics_2_py_
#SBATCH --output=/home/angelos.toutsios.gr/data/Thesis_dev/COCA_statistics/logs/log_%j.out  # Output log file
#SBATCH --error=/home/angelos.toutsios.gr/data/Thesis_dev/COCA_statistics/logs/log_%j.err   # Error log file
#SBATCH -N 2
#SBATCH --mem=120G
#SBATCH --cpus-per-task=64
#SBATCH --time=80:00:00             # Time limit (hh:mm:ss)


python3 -u coca_statistics.py # -u is for printing the outcome directly and not buffer it
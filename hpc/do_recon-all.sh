#!/bin/sh
#SBATCH --partition=container
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --job-name=Jim-recon-all
#SBATCH --output=/home/chingheng/play_ground/recon-all.out
#SBATCH --error=/home/chingheng/play_ground/recon-all.err
module purge
module load singularity/v3.6.2
cd /home/chingheng/play_ground/
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
singularity exec d2is.sif /home/chingheng/play_ground/reconall.sh
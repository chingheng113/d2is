#!/bin/sh
#SBATCH --partition=ai-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=Jim-MRTRIX
#SBATCH --gres=gpu:1
#SBATCH --output=/home/chingheng/play_ground/mrtrix.out
#SBATCH --error=/home/chingheng/play_ground/mrtrix.err
module purge
module load singularity/v3.6.2
cd /home/chingheng/play_ground/org_data_m
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
chmod a+x /home/chingheng/play_ground/org_data_m/mr_step1.sh
singularity exec /home/chingheng/play_ground/mrtrix_nih.sif /home/chingheng/play_ground/org_data_m/mr_step1.sh
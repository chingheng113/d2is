#!/bin/sh
#SBATCH --partition=ai-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --job-name=Jim-MRTRIX
#SBATCH --gres=gpu:1
#SBATCH --output=/home/chingheng/play_ground/step1_mrtrix.out
#SBATCH --error=/home/chingheng/play_ground/step1_mrtrix.err
module purge
module load singularity/v3.6.2
export SINGULARITY_NV=1
cd /home/chingheng/play_ground/org_data_m
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
chmod a+x /home/chingheng/play_ground/org_data_m/mr_step1.sh
time singularity exec /home/chingheng/play_ground/d2is_gpu.sif /home/chingheng/play_ground/org_data_m/mr_step1.sh
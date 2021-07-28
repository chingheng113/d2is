#!/bin/sh
#SBATCH --partition=ai-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --job-name=Jim-FMRIPREP
#SBATCH --gres=gpu:1
#SBATCH --output=/home/chingheng/play_ground/BIDS_tutorial/sub-01.out
#SBATCH --error=/home/chingheng/play_ground/BIDS_tutorial/sub-01.err

module purge
module load singularity/v3.6.2
export SINGULARITY_NV=1
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."


bids_root_dir=$HOME/play_ground/BIDS_tutorial
subj=01

time singularity run $HOME/play_ground/fmriprep_20.2.3.simg \
      $bids_root_dir $bids_root_dir/derivatives \
      participant \
      --participant-label $subj \
      --skip-bids-validation \
      --md-only-boilerplate \
      --fs-license-file $bids_root_dir/license.txt \
      --fs-no-reconall \
      --output-spaces MNI152NLin2009cAsym:res-2 \
      --nthreads 4 \
      --stop-on-first-crash \
      -w $bids_root_dir
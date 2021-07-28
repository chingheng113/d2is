#!/bin/sh
#SBATCH --partition=cputest
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --job-name=Jim-MRTRIX1
#SBATCH --output=/home/chingheng/play_ground/data_m_test/step1_mrtrix.out
#SBATCH --error=/home/chingheng/play_ground/data_m_test/step1_mrtrix.err

module purge
module load singularity/v3.6.2

cd /home/chingheng/play_ground/data_m_test

echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK


chmod a+x /home/chingheng/play_ground/data_m_test/mr_step1.sh

dos2unix /home/chingheng/play_ground/data_m_test/mr_step1.sh

time singularity exec /home/chingheng/play_ground/d2is_gpu.sif /home/chingheng/play_ground/data_m_test/mr_step1.sh

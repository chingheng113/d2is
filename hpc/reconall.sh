#!/bin/sh
cd /home/chingheng/play_ground/data_1
export FREESURFER_HOME=/opt/freesurfer
export SUBJECTS_DIR=/home/chingheng/play_ground/data_1
ls *.nii.gz | parallel --jobs 1 recon-all -parallel -openmp 64 -i {} -s {.}_result -all -qcache
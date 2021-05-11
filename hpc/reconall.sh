#!/bin/sh
cd /home/chingheng/T1WI_org
time ls *.nii.gz | parallel --jobs 1 recon-all -parallel -openmp 64 -i {} -s {.}_result -all -qcache
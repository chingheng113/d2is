#!/bin/sh
cd /home/chingheng/play_ground/data_m
mrconvert MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.nii.gz MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.mif -fslgrad MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.bvec MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.bval
mrinfo -size MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.mif | awk '{print $4}'
dwidenoise MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.mif MRI_0013_20130910_GE_DTI_1b0_1k_62_dir_den.mif -noise noise.mif
mrcalc MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.mif MRI_0013_20130910_GE_DTI_1b0_1k_62_dir_den.mif -subtract residual.mif
mrdegibbs MRI_0013_20130910_GE_DTI_1b0_1k_62_dir.mif MRI_0013_20130910_GE_DTI_1b0_1k_62_dir_den_unr.mif
dwiextract MRI_0013_20130910_GE_DTI_1b0_1k_62_dir_den.mif - -bzero | mrmath - mean mean_b0_AP.mif -axis 3
mrconvert mean_b0_AP.mif mean_b0_AP.nii.gz
flirt -in mean_b0_PA -ref mean_b0_AP -out mean_b0_PA

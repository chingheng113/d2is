#!/bin/bash
#cd dwifslpreproc-tmp-*
cd dwifslpreproc-tmp-MJ346U
totalSlices=`mrinfo dwi.mif | grep Dimensions | awk '{print $6 * $8}'`
totalOutliers=`awk '{ for(i=1;i<=NF;i++)sum+=$i } END { print sum }' dwi_post_eddy.eddy_outlier_map`
echo "If the following number is greater than 10, you may have to discard this subject because of too much motion or corrupted slices"
echo "scale=5; ($totalOutliers / $totalSlices * 100)/1" | bc | tee percentageOutliers.txt
cd ..

dwibiascorrect ants MRI_6946_DTI_1b0_conc_130_dir_den_preproc.mif MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif 
dwi2mask MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif mask.mif

# mrconvert MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif.nii
# bet2 MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif.nii MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased_mask.nii.gz -m -f 0.5
#mrconvert MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased_mask_mask.nii.gz mask.mif 

dwi2response dhollander MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif wm.txt gm.txt csf.txt -voxels voxels.mif
dwi2fod msmt_csd MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif -mask mask.mif wm.txt wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif
mrconvert -coord 3 0 wmfod.mif - | mrcat csffod.mif gmfod.mif - vf.mif 

mtnormalise wmfod.mif wmfod_norm.mif gmfod.mif gmfod_norm.mif csffod.mif csffod_norm.mif -mask mask.mif 

## ANFI + fsl : faster but worse result
# 3dUnifize -input MRI_6946_20210225_Siemens_3D_T1WI_CAC.nii.gz -prefix anat_unifize.nii.gz
# mrconvert anat_unifize.nii.gz AfniT1.mif
# 5ttgen fsl AfniT1.mif 5tt_nocoreg.mif

## same function on fsl: slower but better result
mrconvert MRI_6946_20210225_Siemens_3D_T1WI_CAC.nii.gz fslT1.mif
5ttgen fsl fslT1.mif 5tt_nocoreg.mif

dwiextract MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif - -bzero | mrmath - mean mean_b0.mif -axis 3
mrconvert mean_b0.mif mean_b0.nii.gz
mrconvert 5tt_nocoreg.mif 5tt_nocoreg.nii.gz
fslroi 5tt_nocoreg.nii.gz 5tt_vol0.nii.gz 0 1
flirt -in mean_b0.nii.gz -ref 5tt_vol0.nii.gz -interp nearestneighbour -dof 6 -omat diff2struct_fsl.mat
transformconvert diff2struct_fsl.mat mean_b0.nii.gz 5tt_nocoreg.nii.gz flirt_import diff2struct_mrtrix.txt
mrtransform 5tt_nocoreg.mif -linear diff2struct_mrtrix.txt -inverse 5tt_coreg.mif
5tt2gmwmi 5tt_coreg.mif gmwmSeed_coreg.mif

tckgen -act 5tt_coreg.mif -backtrack -seed_gmwmi gmwmSeed_coreg.mif -nthreads 8 -maxlength 250 -cutoff 0.06 -select 10000000 wmfod_norm.mif tracks_10M.tck


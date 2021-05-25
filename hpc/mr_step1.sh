fslsplit MRI_6946_20210225_Siemens_DTI_1b0_1k_65_dir.nii.gz 
cp vol0000.nii.gz AP.nii.gz
mrconvert AP.nii.gz AP.mif
#mv vol* 1kvol*
for i in `ls vol*`
	do
	mv $i 1k$i
done

fslsplit MRI_6946_20210225_Siemens_DTI_1b0_3k_65_dir.nii.gz
# mv vol* 3kvol*
for i in `ls vol*`
	do
	mv $i 3k$i
done

fslmerge -a MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.nii.gz *vol*

paste MRI_6946_20210225_Siemens_DTI_1b0_1k_65_dir.bvec MRI_6946_20210225_Siemens_DTI_1b0_3k_65_dir.bvec > MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.bvec
paste MRI_6946_20210225_Siemens_DTI_1b0_1k_65_dir.bval MRI_6946_20210225_Siemens_DTI_1b0_3k_65_dir.bval > MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.bval
mrconvert MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.nii.gz MRI_6946_DTI_1b0_conc_130_dir.mif -fslgrad MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.bvec MRI_6946_20210225_Siemens_DTI_1b0_conc_130_dir.bval
rm *vol*
##檢查有幾個方向 ＝130(number): check the result below as 130(number)
##mrinfo -size MRI_6946_DTI_1b0_conc_130_dir.mif | awk '{print $4}'

##dwiw_denoise 
dwidenoise MRI_6946_DTI_1b0_conc_130_dir.mif MRI_6946_DTI_1b0_conc_130_dir_den.mif -noise noise.mif
mrcalc MRI_6946_DTI_1b0_conc_130_dir.mif MRI_6946_DTI_1b0_conc_130_dir_den.mif -subtract residual.mif

##mrview residual.mif
## if you see any clear anatomical landmarks, such as individual gyri or sulci, that may indicate that 
## those parts of the brain have been corrupted by noise. If that happens, you can increase the extent 
## of the denoising filter from the default of 5 to a larger number, such as 7; e.g.,
## dwidenoise your_data.mif your_data_denoised_7extent.mif -extent 7 -noise noise.mif

##mri_degibbs (MRI_6946__DTI_1b0_1k_65_dir_den_unr.mif)
mrdegibbs MRI_6946_DTI_1b0_conc_130_dir.mif MRI_6946_DTI_1b0_conc_130_dir_den_unr.mif


##Extracting the Reverse Phase-Encoded Images (if there is a PA phase)
##fslmerge -t MRI_6946_20210225_Siemens_DTI_PA-phase_enc.dir.nii.gz MRI_6946_20210225_Siemens_DTI_PA-phase_enc.dir.nii.gz MRI_6946_20210225_Siemens_DTI_PA-phase_enc.dir.nii.gz
echo '0'>PA.bval
echo '0'>PA.bvec
echo '0'>>PA.bvec
echo '0'>>PA.bvec

echo '0'>AP.bval
echo '0'>AP.bvec
echo '0'>>AP.bvec
echo '0'>>AP.bvec

# mrconvert MRI_6946_20210225_Siemens_DTI_PA_phase.dir.nii.gz PA.mif -fslgrad MRI_6946_20210225_Siemens_DTI_PA-phase_enc.dir.bvec MRI_6946_20210225_Siemens_DTI_PA-phase_enc.dir.bval - | mrmath - mean mean_b0_PA.mif -axis 3
# mrconvert MRI_6946_20210225_Siemens_DTI_PA_phase.dir.nii.gz mean_b0_PA.mif -fslgrad PA.bval PA.bvec
###### must be following the file order as: bvec, bval
mrconvert MRI_6946_20210225_Siemens_DTI_PA_phase_dir.nii.gz PA.mif 
mrconvert PA.mif PA.mif -fslgrad PA.bvec PA.bval -force
mrconvert AP.mif AP.mif -fslgrad AP.bvec AP.bval -force
##extract the b-values from the primary phase-encoded image, and then combine the two with mrcat
##dwiextract MRI_6946_DTI_1b0_conc_130_dir_den.mif - -bzero | mrmath - mean mean_b0_AP.mif -axis 3 -force
# dwiextract MRI_6946_DTI_1b0_conc_130_dir_den.mif AP.mif -bzero
# mrconvert AP.mif AP.nii.gz


##check mriinfo -size of mean_PA and mean_AP have same dimension, if not, do the folowing, while the input can only be of nii.gz. And change back to mif after it
# mrconvert mean_b0_PA.mif mean_b0_PA.nii.gz
# mrconvert mean_b0_AP.mif mean_b0_AP.nii.gz
mrconvert PA.mif PA.nii.gz -force
mrconvert AP.mif AP.nii.gz -force

# flirt -in mean_b0_PA -ref mean_b0_AP -out mean_b0_PA
flirt -in PA -ref AP -out PA
## PA has one object, and AP has 130 objects(as better reference, instead of vice versa)

# mrconvert mean_b0_PA.nii.gz mean_b0_PA.mif -force
# mrconvert mean_b0_AP.nii.gz mean_b0_AP.mif -force
mrconvert PA.nii.gz PA.mif -force
mrconvert AP.nii.gz AP.mif -force

#######################

# mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_pair.mif
mrcat AP.mif PA.mif -axis 3 b0_pair.mif


##911 AI ##dwifslpreproc (this is very time consuming, please check how this is done)--------
dwifslpreproc MRI_6946_DTI_1b0_conc_130_dir_den.mif MRI_6946_DTI_1b0_conc_130_dir_den_preproc.mif -nocleanup -pe_dir AP -rpe_pair -se_epi b0_pair.mif -eddy_options " --slm=linear --data_is_shelled"

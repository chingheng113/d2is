#!/bin/bash
tckedit tracks_10M.tck -number 200k smallerTracks_200k.tck
#viewmrview MRI_6946_DTI_1b0_conc_130_dir_den_preproc_unbiased.mif  -tractography.load smallerTracks_200k.tck
tcksift2 -act 5tt_coreg.mif -out_mu sift_mu.txt -out_coeffs sift_coeffs.txt -nthreads 8 tracks_10M.tck wmfod_norm.mif sift_1M.txt

labelconvert ./6946_reconall/mri/aparc+aseg.mgz $FREESURFER_HOME/FreeSurferColorLUT.txt /opt/conda/envs/mrtrix/share/mrtrix3/labelconvert/fs_default.txt 6946_parcels.mif
tck2connectome -symmetric -zero_diagonal -scale_invnodevol -tck_weights_in sift_1M.txt tracks_10M.tck 6946_parcels.mif 6946_parcels.csv -out_assignment assignments_6946_parcels.csv
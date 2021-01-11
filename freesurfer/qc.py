import glob
import os

run_id = '1'
root_path = r'\\10.30.9.32\aishare\chingheng\freesurfer_subjects\running_'+run_id
folder_list = glob.glob(root_path+'\\*_result')
for f_path in folder_list:
    img_name = f_path.split('\\')[-1].replace('_result', '')
    scripts = glob.glob(f_path+'\\scripts\\*')
    if os.path.isfile(os.path.join(f_path, 'scripts', 'recon-all.done')):
        os.rename(f_path,
                  f_path.replace('running_'+run_id, 'done'))

        # nii files
        # os.rename(root_path+'\\'+img_name+'.nii',
        #           root_path.replace('running_' + run_id, 'done')+'\\'+img_name+'.nii')

        # GZ files
        os.rename(root_path + '\\' + img_name + '.gz',
                  root_path.replace('running_' + run_id, 'done') + '\\' + img_name + '.gz')
    else:
        print('Bad: %s' %(img_name))
print('done')
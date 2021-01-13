import glob
import os

run_id = '1'
root_path = r'\\10.30.9.32\d2is_images\running_'+run_id
folder_list = glob.glob(root_path+'\\*_result')
for f_path in folder_list:
    img_name = f_path.split('\\')[-1].replace('_result', '')
    scripts = glob.glob(f_path+'\\scripts\\*')
    if os.path.isfile(os.path.join(f_path, 'scripts', 'recon-all.done')):
        # Result folder
        os.rename(f_path,
                  f_path.replace('running_'+run_id, 'data_FS_HPC'))
        # raw file
        os.rename(root_path + '\\' + img_name + '.gz',
                  root_path.replace('running_' + run_id, 'T1WI_processed_HPC') + '\\' + img_name + '.gz')
        print('Good: %s' % (img_name))
    else:
        print('Bad: %s' %(img_name))
print('done')
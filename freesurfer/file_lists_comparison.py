import glob
import os
import shutil
import pandas as pd


def extract_file_name(path_name):
    f_name = path_name.split(os.path.sep)[-1]
    return f_name


target_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'T1WI_org')
source_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'data_FS_KAO')

long_list = glob.glob(os.path.join(target_path, '*'))
long_list = [extract_file_name(p) for p in long_list]
short_list = glob.glob(os.path.join(source_path, '*'))
short_list = [extract_file_name(p) for p in short_list]

i = 0
for s_element in short_list:
    if s_element+'.nii.gz' in long_list:
        try:
            os.rename(os.path.join('\\\\10.30.9.32', 'd2is_images', 'T1WI_org', s_element+'.nii.gz'),
                      os.path.join('\\\\10.30.9.32', 'd2is_images', 'running_pool', s_element+'.nii.gz'))
        except OSError as e:
            print('pass '+s_element)
            pass
    else:
        print(s_element)
        i = i+1
print(i)
print('done')
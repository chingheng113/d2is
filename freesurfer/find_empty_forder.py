import glob
import os

# root_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'data_FS_new_HPC')
# folder_list = glob.glob(root_path+'\\*_result')
root_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'data_FS_KAO')
folder_list = glob.glob(os.path.join(root_path, '*'))
count = 0
for f_path in folder_list:
    img_name = f_path.split('\\')[-1].replace('_result', '')
    content_folder = glob.glob(f_path+'\\*')
    if len(content_folder) == 0:
        print(img_name)
        count = count+1
print('done', count)
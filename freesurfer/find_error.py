import glob
import os

# root_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'data_FS_new_HPC')
# folder_list = glob.glob(root_path+'\\*_result')
root_path = os.path.join('\\\\10.30.9.32', 'd2is_images', 'data_FS_KAO')
folder_list = glob.glob(os.path.join(root_path, '*'))
count = 0
for f_path in folder_list:
    img_name = f_path.split('\\')[-1].replace('_result', '')
    status_log = glob.glob(f_path+'\\scripts\\recon-all-status.log')
    try:
        if len(status_log) > 0:
            with open(status_log[0], 'r', encoding='utf8') as f:
                text = f.read()
                if 'exited with ERRORS' in text:
                    print(img_name)
                    count = count+1
    except:
        print('--', img_name)
print('done', count)
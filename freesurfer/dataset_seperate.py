import glob
import os
import shutil
import pandas as pd

file_list = pd.read_csv('cases.csv', header=None)
for i in ['1', '2', '3']:
    f_count = 0
    for index, row in file_list.iterrows():
        if f_count < 20:
            try:
                # from_path = '\\10.30.9.32\aishare\chingheng\freesurfer_subjects\Chang gung' + row[0]
                # to_path = '\\10.30.9.32\aishare\chingheng\freesurfer_subjects\runnning' + row[0]
                os.rename(r'\\10.30.9.32\aishare\chingheng\freesurfer_subjects\Chang gung'+'\\'+row[0],
                          r'\\10.30.9.32\aishare\chingheng\freesurfer_subjects\running_'+i+'\\'+row[0])
                f_count += 1
            except Exception as e:
                print(e)
                continue

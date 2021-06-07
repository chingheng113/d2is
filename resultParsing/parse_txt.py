#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 13:19:30 2021

@author: anpo
"""

# with open('smb://10.30.9.32/d2is_images/data_FS_new_HPC/MRI_0001_20060909_Philips_3D_T1WI_CAC.nii_result/stats/aseg.stats') as f:
#      lines = f.readlines()
     

# filelist = conn.listPath('d2is_images', '/')

import pandas as pd
import os.path
from smb.SMBConnection import SMBConnection
from smb import smb_structs
smb_structs.SUPPORT_SMB2 = False
import numpy as np

# branch = 'data_FS_new_HPC'
#branch = 'data_FS_KAO'
branch = 'data_FS_new_HPC_re'

conn = SMBConnection('anpo', 'Espesp043!', 'anpolinux', '10.30.9.32', use_ntlm_v2 = True)
conn.connect('10.30.9.32', 139)
sharefolder = 'd2is_images' 
cgmhAI = conn.listPath('d2is_images','/'+branch)
outlist = pd.read_csv('exclude list.csv')


txt_table = {}

txt_table['aseg.stats'] = [1, 79 ,1] # form, start line, column start
txt_table['brainvol.stats'] = [2]           
txt_table['lh.aparc.a2009s.stats'] = [1, 61, 1]
txt_table['lh.aparc.DKTatlas.stats'] = [1, 61, 1]
txt_table['lh.aparc.pial.stats'] = [1, 61, 1]
txt_table['lh.aparc.stats'] = [1, 61, 1] 
txt_table['lh.BA_exvivo.stats'] = [1, 60, 1]
txt_table['lh.BA_exvivo.thresh.stats'] = [1, 60, 1]
txt_table['lh.curv.stats'] = [3]
txt_table['lh.w-g.pct.stats'] = [1, 57, 1]
txt_table['rh.aparc.a2009s.stats'] = [1, 61, 1]
txt_table['rh.aparc.DKTatlas.stats'] = [1, 61, 1]
txt_table['rh.aparc.pial.stats'] = [1, 61, 1]
txt_table['rh.aparc.stats'] = [1, 61, 1]
txt_table['rh.BA_exvivo.stats'] = [1, 60, 1]
txt_table['rh.BA_exvivo.thresh.stats'] = [1, 60, 1]
txt_table['rh.curv.stats'] = [3]
txt_table['rh.w-g.pct.stats'] = [1, 57, 1]
txt_table['wmparc.stats'] = [1, 65, 1]
     

AI_truncated = []
KAO_truncated = []

for key, val in txt_table.items():
    print(key)
    cnt = 0
    s0 = []
    form = val[0]
    if form == 1:
       start_line = val[1]
       offset = val[2]
       
    for i in cgmhAI:
        if cnt>1 and i.filename != '.DS_Store' and i.filename != 'fsaverage' and i.filename != '.':
           # hello = 2
           # print(hello) 
           if i.filename not in outlist:      
              # hello = 1
              # print(hello)
              stat_folder = conn.listPath(sharefolder, os.path.join(branch,i.filename,'stats'))           
              for j in stat_folder:
                  # print(j.filename)
                  # print(key)
                  if j.filename == key:
                      # hello = 3
                      # print(hello)
                      with open('local_file', 'wb') as fp:
                           # name = 'data_FS_KAO/MRI_0004_20060826_Philips_3D_T1WI_CAC/stats/aseg.stats'   
                           # conn.retrieveFileFromOffset(sharefolder, name, fp, offset=0, max_length=-1, timeout=30)
                           # conn.retrieveFile(sharefolder, name, fp)
                           conn.retrieveFile(sharefolder, os.path.join(branch,i.filename,'stats',j.filename), fp)
                                           
                      with open('local_file', 'r') as f:    
                           lines = f.readlines() 
                                  
                      if form == 1:     
                         try: 
                             linestats = lines[start_line:]
                             data = [l.split() for l in linestats]
                             # print(i.filename)
                             # for n in data:
                             rownames = lines[start_line-1].split()
                             data_flat = []
                             data_head = []
                             for inst in data:
                                 cnt2 = 0
                                 inst_ = inst[offset:]
                                 rowname = rownames[-len(inst)+1:]
                                 assert(len(inst_) == len(rowname))                             
                                 for val_1 in inst_:
                                     # if cnt2!=0:   
                                     data_flat.append(val_1)
                                     data_head.append(inst[0]+'-'+rowname[cnt2])
                                     cnt2+=1
                         except:
                            AI_truncated.append(os.path.join(branch,i.filename,'stats',j.filename)) 
                                     
                      elif form == 2:       
                           data_flat = []
                           data_head = []
                           for line in lines:
                               print(line)
                               b = line.split(',')
                               c = b[-3:]
                               data_flat.append(c[1])
                               data_head.append(c[0]+c[2])
                      elif form == 3:                            
                              # # #####
                           data_flat = []
                           data_head = []
                           try:
                               ref = [1, 22, 43, 64, 85, 106, 127, 148, 169, 190]
                               for iline in ref:
                                   idx1 = lines[iline].find('(')
                                   idx2 = lines[iline].find(')')
                                   rowname = lines[iline][idx1+1:idx2]
                                   for cont in range(20):
                                       sline = lines[iline+cont].split(':')
                                       data_flat.append(" ".join(sline[1].split()))
                                       data_head.append(rowname[7:]+'-'+sline[0])
                               other_lines = [211, 212, 213, 214, 215, 217]
                               for olines in other_lines:
                                   sline = lines[olines].split(':')
                                   data_flat.append(" ".join(sline[1].split()))
                                   data_head.append(sline[0])
                           except:    
                               # ref = [1, 22, 43, 64, 85, 106, 127, 148]
                               # for iline in ref:
                               #     idx1 = lines[iline].find('(')
                               #     idx2 = lines[iline].find(')')
                               #     rowname = lines[iline][idx1+1:idx2]
                               #     for cont in range(20):
                               #         sline = lines[iline+cont].split(':')
                               #         data_flat.append(" ".join(sline[1].split()))
                               #         data_head.append(rowname[7:]+'-'+sline[0])
                               # other_lines = [169, 170, 171, 172, 173, 175]
                               # for olines in other_lines:
                               #     sline = lines[olines].split(':')
                               #     data_flat.append(" ".join(sline[1].split()))
                               #     data_head.append(sline[0])
                               KAO_truncated.append(os.path.join(branch,i.filename,'stats',j.filename)) 
                                                       
                      data_ = np.array(data_flat)  
                      
                      subj = {}
                      subj[i.filename] = cnt-2 
                      pdData = pd.DataFrame(data_.reshape(1,-1), index=subj, columns=data_head)             
                      if cnt == 2: 
                         s0 = pdData
                      else:                                          
                         s0 = pd.concat([s0, pdData], axis = 0)       
        cnt += 1
        if cnt%500 == 0:
           print(cnt)
    print(AI_truncated)
    s0.index.name = 'patient ID' 
    s0.to_csv(key+'.csv')
         
     
     
# names = []
# for i in cgmhAI:
#     names.append(i.filename)
     
     
     
     
     
     
     
     
     
# a = conn.listPath('d2is_images','/data_FS_new_HPC/MRI_0001_20060909_Philips_3D_T1WI_CAC.nii_result/stats')


# a = conn.listPath('d2is_images','/data_FS_new_HPC')

# with open('local_file', 'wb') as fp:
#      file_attributes, filesize = conn.retrieveFile('d2is_images','/data_FS_new_HPC/MRI_0001_20060909_Philips_3D_T1WI_CAC.nii_result/stats/aseg.stats', fp)
    
#      # conn.retrieveFile('d2is_images', '/path/to/remote_file', fp)

# with open('local_file', 'r') as f:    
#      lines = f.readlines()






# try:
    
#     conn = SMBConnection('anpo', 'Espesp043!', 'anpolinux', '10.30.9.32', use_ntlm_v2 = True)
#     conn.connect('10.30.9.32', 139)

#     try:
#         Response = conn.listShares(timeout=30)  # obtain a list of shares
#         print('Shares on: ' + system_name)

#         for i in range(len(Response)):  # iterate through the list of shares
#             print("  Share[",i,"] =", Response[i].name)

#             try:
#                 # list the files on each share
#                 Response2 = conn.listPath(Response[i].name,'/',timeout=30)
#                 print('    Files on: ' + system_name + '/' + "  Share[",i,"] =",
#                                        Response[i].name)
#                 for i in range(len(Response2)):
#                     print("    File[",i,"] =", Response2[i].filename)
#             except:
#                 print('### can not access the resource')
#     except:
#         print('### can not list shares')    
# except:
#     print('### can not access the system')















































# remote_address = '10.30.9.32'
# share_name = "public_pictures"
# conn = SMBConnection('anpo', 'Espesp043!', 'anpolinux', '10.30.9.32')
# conn.connect(remote_address)

# file_obj = tempfile.NamedTemporaryFile()
# file_attributes, filesize = conn.retrieveFile('smbtest', '/rfc1001.txt', file_obj)

# # Retrieved file contents are inside file_obj
# # Do what you need with the file_obj and then close it
# # Note that the file obj is positioned at the end-of-file,
# # so you might need to perform a file_obj.seek() if you need
# # to read from the beginning
# file_obj.close()
     
# smb = smbclient.SambaClient(server="10.30.9.32", share="d2is_images",
#                                 username='anpo', password='Espesp043!')
# # print(smb.listdir("/"))
# [u'file1.txt', u'file2.txt']
# >>> f = smb.open('/file1.txt')
# >>> data = f.read()
# >>> f.close()
# >>> smb.rename(u'/file1.txt', u'/file1.old')
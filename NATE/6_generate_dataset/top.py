import os
import shutil
import glob
import pandas as pd
import numpy as np
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
import h5py
from shutil import copyfile
import random
#####################
tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)

################################################################################
dir = '../../Designs/' + design + '/' + tag + '/'
path_number_real_file = open(dir + 'generated_inputs/num_of_paths/num_of_paths.txt', 'r')
path_number_real = path_number_real_file.read().splitlines()
path_number_real_file.close()
num_paths = int(path_number_real[0])
if os.path.exists(dir + 'final_dataset') == True :
	shutil.rmtree(dir + 'final_dataset')
os.makedirs(dir + 'final_dataset_Ali')
############################		input 		################################
df_list = []
# for PT:
for filename in glob.glob(dir + 'NN_training_PT/*.txt'):
	each_file = open(filename, 'r')
	each_file_data = each_file.read().splitlines()
	each_file.close()
	header_name = filename.replace('.txt','')
	header_name = header_name.replace(dir + 'NN_training_PT/','')
	df_list.append(pd.read_table(filename, header=None, names = [header_name]))
	# check the number of generated data:
	if (len(each_file_data) != num_paths):
		print "warning:  PT -- data mismatch data mismatch data mismatch data mismatch data mismatch"
# for ICC:
for filename in glob.glob(dir + 'NN_training_ICC/*.txt'):
	each_file = open(filename, 'r')
	each_file_data = each_file.read().splitlines()
	each_file.close()
	
	header_name = filename.replace('.txt','')
	header_name = header_name.replace(dir + 'NN_training_ICC/','')
	df_list.append(pd.read_table(filename, header=None, names = [header_name]))
	# check the number of generated data:
	if (len(each_file_data) != num_paths):
		print "warning:  ICC -- data mismatch data mismatch data mismatch data mismatch data mismatch"
big_df = pd.concat(df_list, axis=1)
############################		GTM 		################################
slack_GTM = pd.read_csv(dir + 'GTM_slacks_IR_ATA.txt', header=None, names=['GTM'], index_col=False)
#########################		SPICE no HT 		############################
slack_spice = ''
for filename in glob.glob(dir + 'spice/*Slacks.txt'):
	slack_SPICE = open(filename , 'r')
	line_s_spice = slack_SPICE.read().splitlines()
	for i in range(1,len(line_s_spice)):
		slack_spice += (line_s_spice[i]) + '\n'
df_spice = pd.read_csv(StringIO(slack_spice), header=None, names=['index','SPICE_nt'], sep='   ', index_col=0)
df_spice = df_spice.sort_index(inplace=False)
big_df = pd.concat([big_df, df_spice['SPICE_nt']], axis=1)
big_df = pd.concat([big_df, slack_GTM['GTM']*1000], axis=1)
big_df['label'] = big_df['SPICE_nt']
############################		 SPICE  HT 		  ##########################
# HT_dataset_file = open(dir + 'HT_RVT_location_database_updated.txt.txt' , 'r')
# line_HT_dataset = HT_dataset_file.read().splitlines()
# HT_dataset_file.close()
slack_HT = pd.read_csv(dir + 'HT_spice_work/slack_trojan.txt', header=0, sep=' ', index_col=1)
slack_HT = slack_HT.sort_values(by=['path_num'])
big_df['info'] = 'trojan_free'
big_df['status'] = 'train'
########################################################################################
df_HT = pd.read_csv(dir + 'HT_location_database.txt', header=0, sep=' ', index_col=0)
trojan_path_list = []
for i, row in df_HT.iterrows():
	big_df.loc[df_HT.loc[i,'targeted_path_index'],'label'] = slack_HT.loc[df_HT.loc[i,'targeted_path_index'],'slack']
	big_df.loc[df_HT.loc[i,'trigger_path_0'],'label'] = slack_HT.loc[df_HT.loc[i,'trigger_path_0'],'slack']
	big_df.loc[df_HT.loc[i,'trigger_path_1'],'label'] = slack_HT.loc[df_HT.loc[i,'trigger_path_1'],'slack']
	big_df.loc[df_HT.loc[i,'trigger_path_2'],'label'] = slack_HT.loc[df_HT.loc[i,'trigger_path_2'],'slack']
	big_df.loc[df_HT.loc[i,'trigger_path_3'],'label'] = slack_HT.loc[df_HT.loc[i,'trigger_path_3'],'slack']
	#
	big_df.loc[df_HT.loc[i,'targeted_path_index'],'info'] = 'TP'
	big_df.loc[df_HT.loc[i,'trigger_path_0'],'info'] = 'TT'
	big_df.loc[df_HT.loc[i,'trigger_path_1'],'info'] = 'TT'
	big_df.loc[df_HT.loc[i,'trigger_path_2'],'info'] = 'TT'
	big_df.loc[df_HT.loc[i,'trigger_path_3'],'info'] = 'TT'
	# you want to reserve these for evaluation. these should not be in train or test set of NN.
	# later, we pick some of them to force them into trainset
	big_df.loc[df_HT.loc[i,'targeted_path_index'],'status'] = 'eval_detection'
	big_df.loc[df_HT.loc[i,'trigger_path_0'],'status'] = 'eval_detection'
	big_df.loc[df_HT.loc[i,'trigger_path_1'],'status'] = 'eval_detection'
	big_df.loc[df_HT.loc[i,'trigger_path_2'],'status'] = 'eval_detection'
	big_df.loc[df_HT.loc[i,'trigger_path_3'],'status'] = 'eval_detection'
	# record malicious timing paths:
	trojan_path_list.append(df_HT.loc[i,'targeted_path_index'])
	trojan_path_list.append(df_HT.loc[i,'trigger_path_0'])
	trojan_path_list.append(df_HT.loc[i,'trigger_path_1'])
	trojan_path_list.append(df_HT.loc[i,'trigger_path_2'])
	trojan_path_list.append(df_HT.loc[i,'trigger_path_3'])
# label is the difference between SPICE and GTM:
big_df['label'] = big_df['label'] - big_df['GTM']
# now add the paths you want to force them into training set
list_of_random_items = random.sample(trojan_path_list, number_path_included_in_training)
for i in list_of_random_items:
	big_df.loc[i,'status'] = 'train_HT'

big_df.to_csv(dir + 'final_dataset.txt', sep=' ', header=True, index_label='index')

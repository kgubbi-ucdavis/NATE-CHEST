import os
import glob
import pandas as pd
import numpy as np
import def_
import shutil
#############################################################################################
#					 change these variables according to the design							#
#############################################################################################
tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)
#############################################################################################
#############################################################################################
header_remove = ["strength_x4_capture_pt","strength_x2_capture_pt","num_launch_pt","net_m5_capture_pt","net_m3_launch_pt","net_m3_data_pt","net_m3_common_pt","strength_x4_data_pt","strength_x32_data_pt","strength_x16_launch_pt","strength_x16_capture_pt","strength_x0_launch_pt","strength_x0_common_pt","slack_launch_pt","setup_pt","net_m1_data_pt","net_m1_common_pt","strength_x8_common_pt","strength_x2_common_pt","strength_x1_launch_pt","strength_x1_data_pt","strength_x0_capture_pt","slack_capture_pt","num_capture_pt","net_m5_data_pt","net_m4_launch_pt","net_m4_common_pt","strength_x8_data_pt","strength_x4_common_pt","strength_x32_common_pt","strength_x32_capture_pt","strength_x2_launch_pt","strength_x16_data_pt","slack_data_pt","num_data_pt","net_m2_launch_pt","net_m2_common_pt","net_m2_capture_pt","ttl_fanout_pt","strength_x8_launch_pt","strength_x8_capture_pt","strength_x32_launch_pt","strength_x2_data_pt","strength_x1_common_pt","strength_x16_common_pt","strength_x0_data_pt","num_common_pt","net_m4_capture_pt","net_m1_launch_pt","net_m1_capture_pt","strength_x4_launch_pt","strength_x1_capture_pt","net_m5_launch_pt","net_m5_common_pt","net_m4_data_pt","net_m3_capture_pt","net_m2_data_pt"]
print "start"
dirdir = '../../Designs' +  design_name + '/' + Design_tag_name
#############################################################################################
def_.clean_dir(dirdir + '/detection_plot')
print "directory created for " + design_name
#################################################
# making the dataset:
#############		  input 		#############
big_df = pd.read_csv(dirdir + '/final_dataset_before_detection.txt', sep=',', header=0, index_col=0)
big_df = big_df.drop(header_remove,axis=1)

# Stacked:
NN_df = pd.read_csv(dirdir + '/output.csv', header=0, index_col=0)
big_df = big_df.join(NN_df['stacked_ht_0'])
big_df = big_df.join(NN_df['stacked_ht_10'])
big_df = big_df.join(NN_df['stacked_ht_20'])
big_df = big_df.join(NN_df['stacked_ht_30'])
big_df = big_df.join(NN_df['stacked_ht_40'])
big_df = big_df.join(NN_df['stacked_ht_50'])
big_df.rename(columns={'stacked_ht_10': 'stacked_ht_1', 'stacked_ht_20': 'stacked_ht_2', 'stacked_ht_30': 'stacked_ht_3', 'stacked_ht_40': 'stacked_ht_4', 'stacked_ht_50': 'stacked_ht_5'}, inplace=True)
big_df['stacked_ht_0'] = big_df['stacked_ht_0'] - big_df['label']
big_df['stacked_ht_1'] = big_df['stacked_ht_1'] - big_df['label']
big_df['stacked_ht_2'] = big_df['stacked_ht_2'] - big_df['label']
big_df['stacked_ht_3'] = big_df['stacked_ht_3'] - big_df['label']
big_df['stacked_ht_4'] = big_df['stacked_ht_4'] - big_df['label']
big_df['stacked_ht_5'] = big_df['stacked_ht_5'] - big_df['label']
# std of each NN model:
std_df = pd.read_csv(dirdir + '/results.csv', header=0, index_col=0)
std_df_mlp = std_df[(std_df['clf'] == 'mlp')]
std_df_mlp['trj_n'] = int(std_df_mlp['trj_n'])/10
std_df_mlp.set_index('trj_n')
std_df_stacked = std_df[(std_df['clf'] == 'StackingClassifier')]
std_df_stacked['trj_n'] = int(std_df_stacked['trj_n'])/10
std_df_stacked.set_index('trj_n')
# MLP:
big_df = big_df.join(NN_df['mlp_ht_0'])
big_df = big_df.join(NN_df['mlp_ht_10'])
big_df = big_df.join(NN_df['mlp_ht_20'])
big_df = big_df.join(NN_df['mlp_ht_30'])
big_df = big_df.join(NN_df['mlp_ht_40'])
big_df = big_df.join(NN_df['mlp_ht_50'])
big_df.rename(columns={'mlp_ht_10': 'mlp_ht_1', 'mlp_ht_20': 'mlp_ht_2', 'mlp_ht_30': 'mlp_ht_3', 'mlp_ht_40': 'mlp_ht_4', 'mlp_ht_50': 'mlp_ht_5'}, inplace=True)
big_df['mlp_ht_0'] = big_df['mlp_ht_0'] - big_df['label']
big_df['mlp_ht_1'] = big_df['mlp_ht_1'] - big_df['label']
big_df['mlp_ht_2'] = big_df['mlp_ht_2'] - big_df['label']
big_df['mlp_ht_3'] = big_df['mlp_ht_3'] - big_df['label']
big_df['mlp_ht_4'] = big_df['mlp_ht_4'] - big_df['label']
big_df['mlp_ht_5'] = big_df['mlp_ht_5'] - big_df['label']
# SSTA and SGTM:
big_df['ssta'] = big_df['slack_pt'] - big_df['label']
big_df['sgtm'] = big_df['GTM'] - big_df['label']
big_df['ssta'] = big_df['ssta'] + big_df['ssta'].mean(axis = 0)
big_df['sgtm'] = big_df['sgtm'] + big_df['sgtm'].mean(axis = 0)
# youden for SSTA and SGTM:
print "start Youden index calculation for SSTA and SGTM"
youden_ssta = def_.youden(big_df,'ssta')
youden_sgtm = def_.youden(big_df,'sgtm')
# Detection SSTA and SGTM:
detection_ = pd.DataFrame(columns = ['tp_TP_ali_Y','tp_TP_far_Y','tp_TP_ali_sig','tp_TP_far_sig','tp_TP_ali_c','tp_TP_far_c','tp_FP_ali_Y','tp_FP_far_Y','tp_FP_ali_sig','tp_FP_far_sig','tp_FP_ali_c','tp_FP_far_c','tt_TP_ali_Y','tt_TP_far_Y','tt_TP_ali_sig','tt_TP_far_sig','tt_TP_ali_c','tt_TP_far_c','tt_FP_ali_Y','tt_FP_far_Y','tt_FP_ali_sig','tt_FP_far_sig','tt_FP_ali_c','tt_FP_far_c'], index = ['SSTA','SGTM','NGTM-0','NGTM-10','NGTM-20','NGTM-30','NGTM-40','NGTM-50'])
detection_sta_gtm = def_.detection_sta(big_df,45,youden_ssta[0],youden_ssta[1],youden_sgtm[0],youden_sgtm[1])
detection_.loc['SSTA'] = detection_sta_gtm[0]
detection_.loc['SGTM'] = detection_sta_gtm[1]
# Youden index and detection NGTM:
for NN_ in range(6):
	print "model is " + str(NN_)
	# Stacked:
	NN_stacked = 'stacked_ht_' + str(NN_)
	# MLP:
	NN_mlp = 'mlp_ht_' + str(NN_)
	youden_stcked = def_.youden(big_df,NN_stacked)
	youden_mlp = def_.youden(big_df,NN_mlp)
	df_youden_stcked = youden_stcked[2]
	df_youden_mlp = youden_mlp[2]
	df_youden_stcked.to_csv(dirdir + '/detection_plot/youden_stacked' + str(NN_) + '.txt', sep=',', header=True, index_col=True)
	# print df_youden_mlp
	df_youden_mlp.to_csv(dirdir + '/detection_plot/youden_mlp' + str(NN_) + '.txt', sep=',', header=True, index_col=True)
	# Detections: youden tp and tt, sigma, 45ps :
	sigma_stcked = std_df.loc[NN_, 'std_train_stacked']   #?
	std_df.loc[NN_, 'std_train_mlp']   #?
	print "end of NN model " + str(NN_) + " Youden index calculation"
	detection_.loc['NGTM-' + str(10*NN_)] = def_.detection(big_df,NN_,youden_stcked[0],youden_mlp[0],youden_stcked[1],youden_mlp[1],4*sigma_stcked,4*(sigma_mlp+3),45)
	df_net_based = def_.detection_NetBased(big_df,NN_,youden_stcked[0],youden_mlp[0],youden_stcked[1],youden_mlp[1],4*sigma_stcked,4*(sigma_mlp+3),45)
	df_net_based.to_csv(dirdir + '/detection_plot/' + design_name + '_' + str(NN_) + 'net_based.txt', sep=',', header=True, index_col=True)
detection_.to_csv(dirdir + '/detection_plot/' + design_name + '.txt', sep=',', header=True, index_col=True)
print "end for design " + design_name








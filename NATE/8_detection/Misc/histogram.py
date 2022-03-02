import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
#############################################################################################
#					 change these variables according to the design							#
#############################################################################################
design_list = ['S38417','Ethernet','AES128']
# design_list = ['S38417','Ethernet']
# design_list = ['S38417']
#############################################################################################
def y_fmt(y, pos):
	decades = [1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6, 1e-9 ]
	suffix  = ["G", "M", "k", "" , "m" , "u", "n"  ]
	if y == 0:
		return str(0)
	for i, d in enumerate(decades):
		if np.abs(y) >=d:
			val = y/float(d)
			signf = len(str(val).split(".")[1])
			if signf == 0:
				return '{val:d} {suffix}'.format(val=int(val), suffix=suffix[i])
			else:
				if signf == 1:
					# print val, signf
					if str(val).split(".")[1] == "0":
						return '{val:d} {suffix}'.format(val=int(round(val)), suffix=suffix[i]) 
				tx = "{"+"val:.{signf}f".format(signf = signf) +"} {suffix}"
				return tx.format(val=val, suffix=suffix[i])
	return y
#############################################################################################
# df_plot = pd.DataFrame(columns = design_list, index = ['TPR_tp','FPR_tp','ROC_tp','TPR_tt','FPR_tt','ROC_tt'])
header_remove = ["strength_x4_capture_pt","strength_x2_capture_pt","num_launch_pt","net_m5_capture_pt","net_m3_launch_pt","net_m3_data_pt","net_m3_common_pt","strength_x4_data_pt","strength_x32_data_pt","strength_x16_launch_pt","strength_x16_capture_pt","strength_x0_launch_pt","strength_x0_common_pt","slack_launch_pt","setup_pt","net_m1_data_pt","net_m1_common_pt","strength_x8_common_pt","strength_x2_common_pt","strength_x1_launch_pt","strength_x1_data_pt","strength_x0_capture_pt","slack_capture_pt","num_capture_pt","net_m5_data_pt","net_m4_launch_pt","net_m4_common_pt","strength_x8_data_pt","strength_x4_common_pt","strength_x32_common_pt","strength_x32_capture_pt","strength_x2_launch_pt","strength_x16_data_pt","slack_data_pt","num_data_pt","net_m2_launch_pt","net_m2_common_pt","net_m2_capture_pt","ttl_fanout_pt","strength_x8_launch_pt","strength_x8_capture_pt","strength_x32_launch_pt","strength_x2_data_pt","strength_x1_common_pt","strength_x16_common_pt","strength_x0_data_pt","num_common_pt","net_m4_capture_pt","net_m1_launch_pt","net_m1_capture_pt","strength_x4_launch_pt","strength_x1_capture_pt","net_m5_launch_pt","net_m5_common_pt","net_m4_data_pt","net_m3_capture_pt","net_m2_data_pt"]
print "start"
fig_tp, axes_tp = plt.subplots(nrows = 3, ncols = len(design_list), figsize=(10,6))
gs3 = gridspec.GridSpec(3, len(design_list))
gs3.update(hspace=0.44, wspace=0.31)
axes_tp[0][0] = plt.subplot(gs3[0,0])
axes_tp[0][1] = plt.subplot(gs3[0,1])
axes_tp[0][2] = plt.subplot(gs3[0,2])
axes_tp[1][0] = plt.subplot(gs3[1,0])
axes_tp[1][1] = plt.subplot(gs3[1,1])
axes_tp[1][2] = plt.subplot(gs3[1,2])
axes_tp[2][0] = plt.subplot(gs3[2,0])
axes_tp[2][1] = plt.subplot(gs3[2,1])
axes_tp[2][2] = plt.subplot(gs3[2,2])
plot_counter = 0
design_counter = 0
ax_ = [[]]*9
for design_name in design_list:
	dirdir = '/projects/asasan/kgubbi/tvlsi/old_trojan_data/input_NN/' +  design_name
	dirdir_farnaz = '/projects/asasan/kgubbi/tvlsi/old_trojan_data/input_detection_Farnaz/' +  design_name
	dirdir_arash = '/projects/asasan/kgubbi/tvlsi/old_trojan_data/input_detection_Arash/' +  design_name
	#################################################
	# making the dataset:
	#############		  input 		#############
	big_df = pd.read_csv(dirdir + '/final_dataset_before_detection.txt', sep=',', header=0, index_col=0)
	big_df = big_df.drop(header_remove,axis=1)
	# Arash:
	# print design_name
	arash_df = pd.read_csv(dirdir_arash + '/output.csv', header=0, index_col=0)
	# print arash_df
	arash_df = arash_df.sort_index(axis = 0)
	# print arash_df
	big_df = big_df.join(arash_df['ht_0'])
	big_df = big_df.join(arash_df['ht_10'])
	big_df = big_df.join(arash_df['ht_20'])
	big_df = big_df.join(arash_df['ht_30'])
	big_df = big_df.join(arash_df['ht_40'])
	big_df = big_df.join(arash_df['ht_50'])
	big_df.rename(columns={'ht_0': 'arash_0', 'ht_10': 'arash_1', 'ht_20': 'arash_2', 'ht_30': 'arash_3', 'ht_40': 'arash_4', 'ht_50': 'arash_5'}, inplace=True)
	big_df['arash_0'] = big_df['arash_0'] - big_df['label']
	big_df['arash_1'] = big_df['arash_1'] - big_df['label']
	big_df['arash_2'] = big_df['arash_2'] - big_df['label']
	big_df['arash_3'] = big_df['arash_3'] - big_df['label']
	big_df['arash_4'] = big_df['arash_4'] - big_df['label']
	big_df['arash_5'] = big_df['arash_5'] - big_df['label']
	# Ali:
	ali_df = pd.read_csv(dirdir + '/' + design_name + '_old_ali/output.csv', header=0, index_col=0)
	big_df = big_df.join(ali_df['ht_0'])
	big_df = big_df.join(ali_df['ht_10'])
	big_df = big_df.join(ali_df['ht_20'])
	big_df = big_df.join(ali_df['ht_30'])
	big_df = big_df.join(ali_df['ht_40'])
	big_df = big_df.join(ali_df['ht_50'])
	big_df.rename(columns={'ht_0': 'ali_0', 'ht_10': 'ali_1', 'ht_20': 'ali_2', 'ht_30': 'ali_3', 'ht_40': 'ali_4', 'ht_50': 'ali_5'}, inplace=True)
	big_df['ali_0'] = big_df['ali_0'] - big_df['label']
	big_df['ali_1'] = big_df['ali_1'] - big_df['label']
	big_df['ali_2'] = big_df['ali_2'] - big_df['label']
	big_df['ali_3'] = big_df['ali_3'] - big_df['label']
	big_df['ali_4'] = big_df['ali_4'] - big_df['label']
	big_df['ali_5'] = big_df['ali_5'] - big_df['label']
	# Farnaz:
	std_farnaz= []
	for  i in range(6):
		file_ = glob.glob(dirdir_farnaz + '/NN/mode' + str(i) + '_*')[0]
		df_ = pd.read_csv(file_, header=0, index_col=0)
		df_['err'] = df_['predicted_delay'] - df_['delay']
		big_df = big_df.join(df_['predicted_delay'])
		big_df.rename(columns={'predicted_delay': 'farnaz_' + str(i)}, inplace=True)
		big_df['farnaz_' + str(i)] = big_df['farnaz_' + str(i)] + big_df['GTM']
		big_df['farnaz_' + str(i)] = big_df['farnaz_' + str(i)] - big_df['label']
	######################
	ax_[plot_counter] = big_df['arash_3'].hist(bins = 110, ax=axes_tp[0][design_counter])
	ax_[plot_counter].set_title(design_name, fontsize=20, fontweight = 'bold')
	ax_[plot_counter].set_xlim([-100, 100])
	ax_[plot_counter].xaxis.set_ticks([-100,0,100])
	ax_[plot_counter].yaxis.set_major_formatter(FuncFormatter(y_fmt))
	ax_[plot_counter].locator_params(axis='y', nbins=3)
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('Ridge \n ',fontsize=21)
		ax_[plot_counter].yaxis.set_label_coords(-0.22,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	bars = ax_[plot_counter].patches
	for bar in bars:
		bar.set_color('white')
		bar.set_edgecolor('red')
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=19, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=18, size=0)
	######################
	plot_counter += 1
	if design_name == 'S38417':
		ax_[plot_counter] = big_df['farnaz_3'].hist(bins = 110, ax=axes_tp[1][design_counter])
	else:
		ax_[plot_counter] = big_df['farnaz_3'].hist(bins = 100, ax=axes_tp[1][design_counter])
	ax_[plot_counter].set_xlim([-100, 100])
	ax_[plot_counter].xaxis.set_ticks([-100,0,100])
	ax_[plot_counter].yaxis.set_major_formatter(FuncFormatter(y_fmt))
	ax_[plot_counter].locator_params(axis='y', nbins=3)
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('MLP \n ',fontsize=21)
		ax_[plot_counter].yaxis.set_label_coords(-0.22,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	bars = ax_[plot_counter].patches
	for bar in bars:
		bar.set_color('white')
		bar.set_edgecolor('blue')
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=19, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=18, size=0)
	######################
	plot_counter += 1
	ax_[plot_counter] = big_df['ali_3'].hist(bins = 85, ax=axes_tp[2][design_counter])
	ax_[plot_counter].set_xlim([-100, 100])
	ax_[plot_counter].xaxis.set_ticks([-100,0,100])
	ax_[plot_counter].yaxis.set_major_formatter(FuncFormatter(y_fmt))
	ax_[plot_counter].locator_params(axis='y', nbins=5)
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('Stacked \n ',fontsize=21)
		ax_[plot_counter].yaxis.set_label_coords(-0.22,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	ax_[plot_counter].set_xlabel('Error (pSec)',fontsize=20)
	bars = ax_[plot_counter].patches
	for bar in bars:
		bar.set_color('white')
		bar.set_edgecolor('black')
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=19, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=18, size=0)
	######################
	plot_counter += 1
	design_counter += 1
	
	print "end for design " + design_name
fig_tp.savefig('/projects/asasan/kgubbi/tvlsi/scripts/compare_farnaz_ali/histogram.pdf',bbox_inches='tight')







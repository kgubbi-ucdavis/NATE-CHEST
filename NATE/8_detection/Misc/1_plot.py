import os
import glob
import pandas as pd
import numpy as np
import def_
import matplotlib.pyplot as plt
# for plots:
import plot_stacked_bar
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
#############################################################################################
#					 change these variables according to the design							#
#############################################################################################
design_list = ['S38417','Ethernet','AES128']
# design_list = ['S38417','Ethernet']
# design_list = ['S38417']
youden_NN_ = 3
#############################################################################################
# plot Trojan Payload:
fig_tp, axes_tp = plt.subplots(nrows = 3, ncols = len(design_list), figsize=(11,7))
gs2 = gridspec.GridSpec(3, len(design_list))
gs2.update(hspace=0.53)
axes_tp[0][0] = plt.subplot(gs2[0,0])
axes_tp[0][1] = plt.subplot(gs2[0,1])
axes_tp[0][2] = plt.subplot(gs2[0,2])
axes_tp[1][0] = plt.subplot(gs2[1,0])
axes_tp[1][1] = plt.subplot(gs2[1,1])
axes_tp[1][2] = plt.subplot(gs2[1,2])
gs1 = gridspec.GridSpec(3, len(design_list))
gs1.update(hspace=1.00,wspace=1.1,left=0.19,right=0.85)
axes_tp[2][0] = plt.subplot(gs1[2,0])
axes_tp[2][1] = plt.subplot(gs1[2,1])
axes_tp[2][2] = plt.subplot(gs1[2,2])
####################################################
fig_tt, axes_tt = plt.subplots(nrows = 3, ncols = len(design_list), figsize=(11,7))
gs3 = gridspec.GridSpec(3, len(design_list))
gs3.update(hspace=0.52)
axes_tt[0][0] = plt.subplot(gs3[0,0])
axes_tt[0][1] = plt.subplot(gs3[0,1])
axes_tt[0][2] = plt.subplot(gs3[0,2])
axes_tt[1][0] = plt.subplot(gs3[1,0])
axes_tt[1][1] = plt.subplot(gs3[1,1])
axes_tt[1][2] = plt.subplot(gs3[1,2])
gs4 = gridspec.GridSpec(3, len(design_list))
gs4.update(hspace=1.00,wspace=1.1,left=0.19,right=0.85)
axes_tt[2][0] = plt.subplot(gs4[2,0])
axes_tt[2][1] = plt.subplot(gs4[2,1])
axes_tt[2][2] = plt.subplot(gs4[2,2])
# hatches and colors:
hatches = [None,None,None,None,None,None,None,None,None,None,'///','///','///','///','///','///',None,None,None,None,None,None,None,None,'///','///','///','///','///','///','///','///']
col_ = ['dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','dodgerblue','black','black','red','red','red','red','red','red','red','red','red','red','red','red','red','red']
####################################################
plot_counter = 0
design_counter = 0
ax_ = [[]]*18
#############################################################################################
for design_name in design_list:
	dirdir = '/projects/asasan/avakil/tvlsi/old_trojan_data/input_NN/' +  design_name
	#############################################################################################
	detection_ = pd.read_csv(dirdir + '/detection_plot/' + design_name + '.csv', sep=',', header=0, index_col=0)
	df_youden_ali = pd.read_csv(dirdir + '/detection_plot/youden_' + str(youden_NN_) + '.txt', sep=',', header=0, index_col=0)
	df_youden_farnaz = pd.read_csv(dirdir + '/detection_plot/youden_' + str(youden_NN_) + '.txt', sep=',', header=0, index_col=0)
	#################################
	#			ROC curves:			#
	#################################
	# plot tp ROC curves:
	ax_[plot_counter] = df_youden_ali.plot.line(x='FP_ratio', y='TP_tp_ratio', color = 'r', linewidth=2, ax=axes_tp[2][design_counter])
	ax_[plot_counter] = df_youden_farnaz.plot.line(x='FP_ratio', y='TP_tp_ratio', color = 'b',linewidth=2, ax=axes_tp[2][design_counter])
	ax_[plot_counter].set_xlim([-0.01, 1.01])
	ax_[plot_counter].set_ylim([-0.01, 1.01])
	ax_[plot_counter].set_xticks((0,1))
	ax_[plot_counter].set_yticks((0,1))
	ax_[plot_counter].set_ylabel('TPR',fontsize=12)
	ax_[plot_counter].set_xlabel('FPR',fontsize=12)
	ax_[plot_counter].set_title('ROC', fontsize=12, fontweight = 'bold')
	ax_[plot_counter].get_legend().remove()
	plot_counter += 1
	# plot tt ROC curves:
	ax_[plot_counter] = df_youden_ali.plot.line(x='FP_ratio', y='TP_tt_ratio', color = 'r', linewidth=2, ax=axes_tt[2][design_counter])
	ax_[plot_counter] = df_youden_farnaz.plot.line(x='FP_ratio', y='TP_tt_ratio', color = 'b', linewidth=2, ax=axes_tt[2][design_counter])
	ax_[plot_counter].set_xlim([-0.01, 1.01])
	ax_[plot_counter].set_ylim([-0.01, 1.01])
	ax_[plot_counter].set_xticks((0,1))
	ax_[plot_counter].set_yticks((0,1))
	ax_[plot_counter].set_ylabel('TPR',fontsize=12)
	ax_[plot_counter].set_xlabel('FPR',fontsize=12)
	ax_[plot_counter].set_title('ROC', fontsize=12, fontweight = 'bold')
	ax_[plot_counter].get_legend().remove()
	plot_counter += 1
	#################################
	#			TP curves:			#
	#################################
	# plot tp TP:
	detection_plot = detection_.drop(['tp_TP_ali_c','tp_TP_far_c','tp_FP_ali_Y','tp_FP_far_Y','tp_FP_ali_sig','tp_FP_far_sig','tp_FP_ali_c','tp_FP_far_c','tt_TP_ali_Y','tt_TP_far_Y','tt_TP_ali_sig','tt_TP_far_sig','tt_TP_ali_c','tt_TP_far_c','tt_FP_ali_Y','tt_FP_far_Y','tt_FP_ali_sig','tt_FP_far_sig','tt_FP_ali_c','tt_FP_far_c'], axis=1)
	ax_[plot_counter] = detection_plot.plot.bar(stacked=False, width=0.8, ax=axes_tp[0][design_counter])
	ax_[plot_counter].get_legend().remove()
	ax_[plot_counter].set_ylim([0, 100])
	# ax_[plot_counter].yaxis.set_ticks(np.arange(0,100,25))
	ax_[plot_counter].set_title(design_name, fontsize=13, fontweight = 'bold')
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('% True Positive',fontsize=12)
		ax_[plot_counter].yaxis.set_label_coords(-0.13,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=10, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=9, size=0)
	# add color and hatches:
	bars = ax_[plot_counter].patches
	for bar, hatch, col in zip(bars, hatches, col_):
		bar.set_color(col)
		bar.set_edgecolor('white')
		bar.set_hatch(hatch)
	plot_counter += 1
	# plot tp FP:
	detection_plot = detection_.drop(['tp_FP_ali_c','tp_FP_far_c','tp_TP_ali_Y','tp_TP_far_Y','tp_TP_ali_sig','tp_TP_far_sig','tp_TP_ali_c','tp_TP_far_c','tt_TP_ali_Y','tt_TP_far_Y','tt_TP_ali_sig','tt_TP_far_sig','tt_TP_ali_c','tt_TP_far_c','tt_FP_ali_Y','tt_FP_far_Y','tt_FP_ali_sig','tt_FP_far_sig','tt_FP_ali_c','tt_FP_far_c'], axis=1)
	ax_[plot_counter] = detection_plot.plot.bar(stacked=False, width=0.8, ax=axes_tp[1][design_counter])
	ax_[plot_counter].get_legend().remove()
	ax_[plot_counter].set_ylim([0, 50])
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('% False Positive',fontsize=12)
		ax_[plot_counter].yaxis.set_label_coords(-0.13,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=10, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=9, size=0)
	bars = ax_[plot_counter].patches
	for bar, hatch, col in zip(bars, hatches, col_):
		bar.set_color(col)
		bar.set_edgecolor('white')
		bar.set_hatch(hatch)
	plot_counter += 1
	#################################
	#			TT curves:			#
	#################################
	# plot tt TP:
	detection_plot = detection_.drop(['tt_TP_ali_c','tt_TP_far_c','tp_TP_ali_Y','tp_TP_far_Y','tp_TP_ali_sig','tp_TP_far_sig','tp_TP_ali_c','tp_TP_far_c','tp_FP_ali_Y','tp_FP_far_Y','tp_FP_ali_sig','tp_FP_far_sig','tp_FP_ali_c','tp_FP_far_c','tt_FP_ali_Y','tt_FP_far_Y','tt_FP_ali_sig','tt_FP_far_sig','tt_FP_ali_c','tt_FP_far_c'], axis=1)
	ax_[plot_counter] = detection_plot.plot.bar(stacked=False, width=0.8, ax=axes_tt[0][design_counter])
	ax_[plot_counter].get_legend().remove()
	ax_[plot_counter].set_ylim([0, 100])
	# ax_[plot_counter].yaxis.set_ticks(np.arange(0,100,25))
	ax_[plot_counter].set_title(design_name, fontsize=13, fontweight = 'bold')
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('% True Positive',fontsize=12)
		ax_[plot_counter].yaxis.set_label_coords(-0.13,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=10, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=9, size=0)
	bars = ax_[plot_counter].patches
	for bar, hatch, col in zip(bars, hatches, col_):
		bar.set_color(col)
		bar.set_edgecolor('white')
		bar.set_hatch(hatch)
	plot_counter += 1
	# plot tt FP:
	detection_plot = detection_.drop(['tt_FP_ali_c','tt_FP_far_c','tp_TP_ali_Y','tp_TP_far_Y','tp_TP_ali_sig','tp_TP_far_sig','tp_TP_ali_c','tp_TP_far_c','tp_FP_ali_Y','tp_FP_far_Y','tp_FP_ali_sig','tp_FP_far_sig','tp_FP_ali_c','tp_FP_far_c','tt_TP_ali_Y','tt_TP_far_Y','tt_TP_ali_sig','tt_TP_far_sig','tt_TP_ali_c','tt_TP_far_c'], axis=1)
	ax_[plot_counter] = detection_plot.plot.bar(stacked=False, width=0.8, ax=axes_tt[1][design_counter])
	ax_[plot_counter].get_legend().remove()
	ax_[plot_counter].set_ylim([0, 50])
	if design_name == 'S38417':
		ax_[plot_counter].set_ylabel('% False Positive',fontsize=12)
		ax_[plot_counter].yaxis.set_label_coords(-0.13,0.5)
	else:
		ax_[plot_counter].set_ylabel('',fontsize=10)
	ax_[plot_counter].tick_params(axis='y', which='major', labelsize=10, gridOn='-')
	ax_[plot_counter].tick_params(axis='x', which='major', labelsize=9, size=0)
	bars = ax_[plot_counter].patches
	for bar, hatch, col in zip(bars, hatches, col_):
		bar.set_color(col)
		bar.set_edgecolor('white')
		bar.set_hatch(hatch)
	plot_counter += 1
	#
	design_counter += 1
#############################################################################################
labels = ['$Youden$','$45 ps$', '$4 \sigma$','$MLP$','$Stacked$','$MLP$','$Stacked$']
hndels = []
hndels.append(Patch(facecolor='dodgerblue', edgecolor='w'))
hndels.append(Patch(facecolor='black', edgecolor='w'))
hndels.append(Patch(facecolor='red', edgecolor='w'))
hndels.append(Patch(facecolor='w', hatch='////', edgecolor='black'))
hndels.append(Patch(facecolor='w', edgecolor='black'))
hndels.append(Line2D([0], [0], color='b', linewidth=2))
hndels.append(Line2D([0], [0], color='r', linewidth=2))

fig_tp.legend(hndels, labels, loc='lower center', ncol = 7, fontsize='small', bbox_to_anchor=(0.45, -0.006))
fig_tt.legend(hndels, labels, loc='lower center', ncol = 7, fontsize='small', bbox_to_anchor=(0.45, -0.007))

fig_tp.savefig('/projects/asasan/avakil/tvlsi/designs/fig_tp.pdf',bbox_inches='tight')
fig_tt.savefig('/projects/asasan/avakil/tvlsi/designs/fig_tt.pdf',bbox_inches='tight')





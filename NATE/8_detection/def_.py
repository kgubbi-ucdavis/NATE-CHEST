import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shutil
#############################################################################################
def clean_dir(dir_):
	if os.path.exists(dir_) == True :
		shutil.rmtree(dir_)
	os.makedirs(dir_)
	return()
#############################################################################################
def youden(in_,NN_model):
	Youden_ = pd.DataFrame({'thresholds':[-200,-150,-100,-80,-70,-60,-55,-50,-45,-40,-35,-30,-25,-20,-15,-10,-5,0,0.1,0.3,0.5,0.7,0.9,1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95,97,99,101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187,189,191,193,195,197,199,201,203,205,207,209,211,213,215,217,219,221,223,225,227,229,231,233,235,237,239,241,243,245,247,249,251,253,255,257,259,261,263,265,267,269,271,273,275,277,279,281,283,285,287,289,291,293,295,297,299,301,303,305,307,309,311,313,315]})
	# Youden_ = pd.DataFrame({'thresholds':[0.1,0.7,0.9,1,5,10,30,50]})
	Youden_['TP_tp_ratio'] = ''
	Youden_['TP_tt_ratio'] = ''
	Youden_['FP_ratio'] = ''
	Youden_['Youden_tp'] = ''
	Youden_['Youden_tt'] = ''
	for j,rows in Youden_.iterrows():
		threshold_ = Youden_.loc[j,'thresholds']
		TP_tp = 0
		TP_tt = 0
		FP = 0
		for i,row in in_.iterrows():
			if (in_.loc[i,NN_model] >= float(threshold_)) and (int(i) in range(700,745)):
				TP_tp += 1
			if (in_.loc[i,NN_model] >= float(threshold_)) and (int(i) in range(745,790)):
				TP_tt += 1
			if (in_.loc[i,NN_model] >= float(threshold_)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
				FP += 1
		Youden_.loc[j,'TP_tp_ratio'] = float(TP_tp)/45
		Youden_.loc[j,'TP_tt_ratio'] = float(TP_tt)/45
		Youden_.loc[j,'FP_ratio'] = float(FP)/(len(in_.index)-180)
		Youden_.loc[j,'Youden_tp'] = (float(TP_tp)/45) - (float(FP)/len(in_.index))
		Youden_.loc[j,'Youden_tt'] = (float(TP_tt)/45) - (float(FP)/len(in_.index))
	youden_tp_max = Youden_.loc[Youden_['Youden_tp'].idxmax(),'thresholds']
	youden_tt_max = Youden_.loc[Youden_['Youden_tt'].idxmax(),'thresholds']
	return(youden_tp_max, youden_tt_max, Youden_)
	
def detection(in_,NN_model,Y_ali_tp,Y_far_tp,Y_ali_tt,Y_far_tt,sig_ali,sig_far,c_):
	# ali:
	NN_ali = 'stacked_ht_' + str(NN_model)
	# farnaz:
	NN_far = 'mlp_ht_' + str(NN_model)
	# trojan payload:
	TP_tp_Y_ali = 0
	TP_tp_Y_far = 0
	TP_tp_sig_ali = 0
	TP_tp_sig_far = 0
	TP_tp_c_ali = 0
	TP_tp_c_far = 0
	# trojan trigger:
	TP_tt_Y_ali = 0
	TP_tt_Y_far = 0
	TP_tt_sig_ali = 0
	TP_tt_sig_far = 0
	TP_tt_c_ali = 0
	TP_tt_c_far = 0
	# False Positive:
	FP_Y_ali_tp = 0
	FP_Y_ali_tt = 0
	FP_Y_far_tp = 0
	FP_Y_far_tt = 0
	FP_sig_ali = 0
	FP_sig_far = 0
	FP_c_ali = 0
	FP_c_far = 0
	################
	for i,row in in_.iterrows():
		# Ali tp:
		if (in_.loc[i,NN_ali] >= float(Y_ali_tp)) and (int(i) in range(700,745)):
			TP_tp_Y_ali += 1
		if (in_.loc[i,NN_ali] >= float(sig_ali)) and (int(i) in range(700,745)):
			TP_tp_sig_ali += 1
		if (in_.loc[i,NN_ali] >= float(c_)) and (int(i) in range(700,745)):
			TP_tp_c_ali += 1
		# Farnaz tp:
		if (in_.loc[i,NN_far] >= float(Y_far_tp)) and (int(i) in range(700,745)):
			TP_tp_Y_far += 1
		if (in_.loc[i,NN_far] >= float(sig_far)) and (int(i) in range(700,745)):
			TP_tp_sig_far += 1
		if (in_.loc[i,NN_far] >= float(c_)) and (int(i) in range(700,745)):
			TP_tp_c_far += 1
		# Ali tt:
		if (in_.loc[i,NN_ali] >= float(Y_ali_tt)) and (int(i) in range(745,790)):
			TP_tt_Y_ali += 1
		if (in_.loc[i,NN_ali] >= float(sig_ali)) and (int(i) in range(745,790)):
			TP_tt_sig_ali += 1
		if (in_.loc[i,NN_ali] >= float(c_)) and (int(i) in range(745,790)):
			TP_tt_c_ali += 1
		# Farnaz tt:
		if (in_.loc[i,NN_far] >= float(Y_far_tt)) and (int(i) in range(745,790)):
			TP_tt_Y_far += 1
		if (in_.loc[i,NN_far] >= float(sig_far)) and (int(i) in range(745,790)):
			TP_tt_sig_far += 1
		if (in_.loc[i,NN_far] >= float(c_)) and (int(i) in range(745,790)):
			TP_tt_c_far += 1
		# False Positive:
		# Ali
		if (in_.loc[i,NN_ali] >= float(Y_ali_tp)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_ali_tp += 1
		if (in_.loc[i,NN_ali] >= float(Y_ali_tt)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_ali_tt += 1
		if (in_.loc[i,NN_ali] >= float(sig_ali)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_sig_ali += 1
		if (in_.loc[i,NN_ali] >= float(c_)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_c_ali += 1
		# Farnaz
		if (in_.loc[i,NN_far] >= float(Y_far_tp)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_far_tp += 1
		if (in_.loc[i,NN_far] >= float(Y_far_tt)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_far_tt += 1
		if (in_.loc[i,NN_far] >= float(sig_far)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_sig_far += 1
		if (in_.loc[i,NN_far] >= float(c_)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_c_far += 1
	# tp ratios:
	TP_tp_ratio_ali_Y = (float(TP_tp_Y_ali)/45)*100
	TP_tp_ratio_far_Y = (float(TP_tp_Y_far)/45)*100
	TP_tp_ratio_ali_sigma = (float(TP_tp_sig_ali)/45)*100
	TP_tp_ratio_far_sigma = (float(TP_tp_sig_far)/45)*100
	TP_tp_ratio_ali_c = (float(TP_tp_c_ali)/45)*100
	TP_tp_ratio_far_c = (float(TP_tp_c_far)/45)*100
	# tt ratios
	TP_tt_ratio_ali_Y = (float(TP_tt_Y_ali)/45)*100
	TP_tt_ratio_far_Y = (float(TP_tt_Y_far)/45)*100
	TP_tt_ratio_ali_sigma = (float(TP_tt_sig_ali)/45)*100
	TP_tt_ratio_far_sigma = (float(TP_tt_sig_far)/45)*100
	TP_tt_ratio_ali_c = (float(TP_tt_c_ali)/45)*100
	TP_tt_ratio_far_c = (float(TP_tt_c_far)/45)*100
	# FP ratio
	FP_ratio_ali_Y_tp = (float(FP_Y_ali_tp)/(len(in_.index)-180))*100
	FP_ratio_far_Y_tp = (float(FP_Y_far_tp)/(len(in_.index)-180))*100
	FP_ratio_ali_sig_tp = (float(FP_sig_ali)/(len(in_.index)-180))*100
	FP_ratio_far_sig_tp = (float(FP_sig_far)/(len(in_.index)-180))*100
	FP_ratio_ali_c_tp = (float(FP_c_ali)/(len(in_.index)-180))*100
	FP_ratio_far_c_tp = (float(FP_c_far)/(len(in_.index)-180))*100
	#
	FP_ratio_ali_Y_tt = (float(FP_Y_ali_tt)/(len(in_.index)-180))*100
	FP_ratio_far_Y_tt = (float(FP_Y_far_tt)/(len(in_.index)-180))*100
	FP_ratio_ali_sig_tt = (float(FP_sig_ali)/(len(in_.index)-180))*100
	FP_ratio_far_sig_tt = (float(FP_sig_far)/(len(in_.index)-180))*100
	FP_ratio_ali_c_tt = (float(FP_c_ali)/(len(in_.index)-180))*100
	FP_ratio_far_c_tt = (float(FP_c_far)/(len(in_.index)-180))*100
	return([TP_tp_ratio_ali_Y,TP_tp_ratio_far_Y,TP_tp_ratio_ali_sigma,TP_tp_ratio_far_sigma,TP_tp_ratio_ali_c,TP_tp_ratio_far_c,FP_ratio_ali_Y_tp,FP_ratio_far_Y_tp,FP_ratio_ali_sig_tp,FP_ratio_far_sig_tp,FP_ratio_ali_c_tp,FP_ratio_far_c_tp,TP_tt_ratio_ali_Y,TP_tt_ratio_far_Y,TP_tt_ratio_ali_sigma,TP_tt_ratio_far_sigma,TP_tt_ratio_ali_c,TP_tt_ratio_far_c,FP_ratio_ali_Y_tt,FP_ratio_far_Y_tt,FP_ratio_ali_sig_tt,FP_ratio_far_sig_tt,FP_ratio_ali_c_tt,FP_ratio_far_c_tt])

def detection_sta(in_,c_,Y_sta_tp,Y_sta_tt,Y_gtm_tp,Y_gtm_tt):
	# trojan payload:
	TP_tp_Y_sta = 0
	TP_tp_Y_gtm = 0
	TP_tp_c_sta = 0
	TP_tp_c_gtm = 0
	# trojan trigger:
	TP_tt_Y_sta = 0
	TP_tt_Y_gtm = 0
	TP_tt_c_sta = 0
	TP_tt_c_gtm = 0
	# False Positive:
	FP_Y_sta_tp = 0
	FP_Y_gtm_tp = 0
	FP_Y_sta_tt = 0
	FP_Y_gtm_tt = 0
	FP_c_sta = 0
	FP_c_gtm = 0
	################
	for i,row in in_.iterrows():
		# sta tp:
		if (in_.loc[i,'ssta'] >= float(Y_sta_tp)) and (int(i) in range(700,745)):
			TP_tp_Y_sta += 1
		if (in_.loc[i,'ssta'] >= float(c_)) and (int(i) in range(700,745)):
			TP_tp_c_sta += 1
		# gtm tp:
		if (in_.loc[i,'sgtm'] >= float(Y_gtm_tp)) and (int(i) in range(700,745)):
			TP_tp_Y_gtm += 1
		if (in_.loc[i,'sgtm'] >= float(c_)) and (int(i) in range(700,745)):
			TP_tp_c_gtm += 1
		# sta tt:
		if (in_.loc[i,'ssta'] >= float(Y_sta_tt)) and (int(i) in range(745,790)):
			TP_tt_Y_sta += 1
		if (in_.loc[i,'ssta'] >= float(c_)) and (int(i) in range(745,790)):
			TP_tt_c_sta += 1
		# gtm tt:
		if (in_.loc[i,'sgtm'] >= float(Y_gtm_tt)) and (int(i) in range(745,790)):
			TP_tt_Y_gtm += 1
		if (in_.loc[i,'sgtm'] >= float(c_)) and (int(i) in range(745,790)):
			TP_tt_c_gtm += 1
		# False Positive:
		# sta
		if (in_.loc[i,'ssta'] >= float(Y_sta_tp)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_sta_tp += 1
		if (in_.loc[i,'ssta'] >= float(Y_sta_tt)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_sta_tt += 1
		if (in_.loc[i,'ssta'] >= float(c_)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_c_sta += 1
		# gtm
		if (in_.loc[i,'sgtm'] >= float(Y_gtm_tp)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_gtm_tp += 1
		if (in_.loc[i,'sgtm'] >= float(Y_gtm_tt)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_Y_gtm_tt += 1
		if (in_.loc[i,'sgtm'] >= float(c_)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			FP_c_gtm += 1
	# tp ratios:
	TP_tp_ratio_sta_Y = (float(TP_tp_Y_sta)/45)*100
	TP_tp_ratio_gtm_Y = (float(TP_tp_Y_gtm)/45)*100
	TP_tp_ratio_sta_c = (float(TP_tp_c_sta)/45)*100
	TP_tp_ratio_gtm_c = (float(TP_tp_c_gtm)/45)*100
	# tt ratios
	TP_tt_ratio_sta_Y = (float(TP_tt_Y_sta)/45)*100
	TP_tt_ratio_gtm_Y = (float(TP_tt_Y_gtm)/45)*100
	TP_tt_ratio_sta_c = (float(TP_tt_c_sta)/45)*100
	TP_tt_ratio_gtm_c = (float(TP_tt_c_gtm)/45)*100
	# FP ratio
	FP_ratio_sta_Y_tp = (float(FP_Y_sta_tp)/(len(in_.index)-180))*100
	FP_ratio_gtm_Y_tp = (float(FP_Y_gtm_tp)/(len(in_.index)-180))*100
	FP_ratio_sta_c_tp = (float(FP_c_sta)/(len(in_.index)-180))*100
	FP_ratio_gtm_c_tp = (float(FP_c_gtm)/(len(in_.index)-180))*100
	#
	FP_ratio_sta_Y_tt = (float(FP_Y_sta_tt)/(len(in_.index)-180))*100
	FP_ratio_gtm_Y_tt = (float(FP_Y_gtm_tt)/(len(in_.index)-180))*100
	FP_ratio_sta_c_tt = (float(FP_c_sta)/(len(in_.index)-180))*100
	FP_ratio_gtm_c_tt = (float(FP_c_gtm)/(len(in_.index)-180))*100
	return([0,TP_tp_ratio_sta_Y,TP_tp_ratio_sta_c,0,'NA','NA',0,FP_ratio_sta_Y_tp,FP_ratio_sta_c_tp,0,'NA','NA',0,TP_tt_ratio_sta_Y,TP_tt_ratio_sta_c,0,'NA','NA',0,FP_ratio_sta_Y_tt,FP_ratio_sta_c_tt,0,'NA','NA'],[0,TP_tp_ratio_gtm_Y,TP_tp_ratio_gtm_c,0,'NA','NA',0,FP_ratio_gtm_Y_tp,FP_ratio_gtm_c_tp,0,'NA','NA',0,TP_tt_ratio_gtm_Y,TP_tt_ratio_gtm_c,0,'NA','NA',0,FP_ratio_gtm_Y_tt,FP_ratio_gtm_c_tt,0,'NA','NA'])

def detection_NetBased(in_,NN_model,Y_ali_tp,Y_far_tp,Y_ali_tt,Y_far_tt,sig_ali,sig_far,c_):
	# table of info for net based detection:
	df_ = in_
	df_["TP_stacked"] = "clean"
	df_["TP_mlp"] = "clean"
	df_["TT_stacked"] = "clean"
	df_["TT_mlp"] = "clean"
	df_["FP_stacked"] = "clean"
	df_["FP_mlp"] = "clean"
	# stacked:
	NN_stacked = 'stacked_ht_' + str(NN_model)
	# mlp:
	NN_mlp = 'mlp_ht_' + str(NN_model)
	################
	for i,row in in_.iterrows():
		# stacked tp:
		if (in_.loc[i,NN_stacked] >= float(sig_ali)) and (int(i) in range(700,745)):
			df_.loc[i,"TP_stacked"] = "Detected"
		# mlp tp:
		if (in_.loc[i,NN_mlp] >= float(sig_far)) and (int(i) in range(700,745)):
			df_.loc[i,"TP_mlp"] = "Detected"
		# stacked tt:
		if (in_.loc[i,NN_stacked] >= float(sig_ali)) and (int(i) in range(745,790)):
			df_.loc[i,"TT_stacked"] = "Detected"
		# mlp tt:
		if (in_.loc[i,NN_mlp] >= float(sig_far)) and (int(i) in range(745,790)):
			df_.loc[i,"TT_mlp"] = "Detected"
		# False Positive:
		# stacked
		if (in_.loc[i,NN_stacked] >= float(sig_ali)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			df_.loc[i,"FP_stacked"] = "Detected"
		# mlp
		if (in_.loc[i,NN_mlp] >= float(sig_far)) and (int(i) not in range(700,790)) and (int(i) not in range(900,990)):
			df_.loc[i,"FP_mlp"] = "Detected"
	return(df_)



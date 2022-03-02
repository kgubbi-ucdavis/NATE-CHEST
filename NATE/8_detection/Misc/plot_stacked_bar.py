import pandas as pd
import matplotlib
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import seaborn
#
###################################       define function to plot       ###################################
def plot_clustered_stacked(dfall, labels=None, title="",  H="/", **kwargs):
	"""Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
	labels is a list of the names of the dataframe, used for the legend
	title is a string for the title of the plot
	H is the hatch used for identification of the different dataframe"""
	n_df = len(dfall)
	n_col = len(dfall[0].columns) 
	n_ind = len(dfall[0].index)
	axe = plt.subplot(111)
	hattch = ['' , '\\', '///////', '*', 'o', 'x', '+','','','','','','']
	for df in dfall : # for each data frame
		axe = df.plot(kind="bar",
		linewidth=1,
		stacked=True,
		ax=axe,
		legend=False,
		grid=False,
		edgecolor="black",
		**kwargs)  # make bar plots
	
	h,l = axe.get_legend_handles_labels() # get the handles we want to modify
	for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
		for j, pa in enumerate(h[i:i+n_col]):
			for rect in pa.patches: # for each index
				rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
				# rect.set_hatch(H * int(i / n_col)) #edited part     
				rect.set_hatch(hattch[int(i / n_col)]) #edited part     
				rect.set_width(1 / float(n_df + 1))
	
	axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
	axe.set_xticklabels(df.index, rotation = 90, fontweight='bold')
	axe.set_ylabel('Percentage Detection' ,fontweight='bold',fontsize=29)
	axe.set_xlabel('' ,fontweight='bold',fontsize=24)
	axe.set_title(title,fontsize=26,)
	axe.xaxis.set_tick_params(labelsize=28, length=0)
	axe.yaxis.set_tick_params(labelsize=34)
	# Add invisible data to add another legend
	n=[]
	for i in range(n_df):
		# n.append(axe.bar(0, 0, color="gray", hatch=H * i))
		n.append(axe.bar(0, 0, color="gray", hatch=hattch[i]))

	l1 = axe.legend(h[0:n_col], l[:n_col], loc=[1.01, 0.5],fontsize='xx-large')
	if labels is not None:
		l2 = plt.legend(n, labels, loc=[1.01, 0.1],fontsize='xx-large') 
	axe.add_artist(l1)
	return axe
###########################################################################################################
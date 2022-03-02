import os
import numpy as np
import math 
import subprocess
import shutil
from shutil import copyfile
from run_SPICE import spice_run
#############################################################################################
tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)
Design_folder_name = Design_name
os.environ['clock_ports'] = clock_ports_name
design_cel = top_name_
os.environ['sdc_of_pt']= constraint_dir
os.environ['mw_of_pt']= milkyway_lib_dir
V_min = float(V_min)
V_max = float(V_max)
spf_lib_ = spf_lib_
spice_lib_ = spf_lib_
os.environ['target_'] = target_lib_
os.environ['scaling_lib_1'] = scaling_lib_1
os.environ['scaling_lib_2'] = scaling_lib_2
os.environ['scaling_lib_3'] = scaling_lib_3
os.environ['search_path_'] = search_path_
#############################################################################################
#									 making folders											#
#############################################################################################
os.environ['workfolder_of_pt']= '../../Designs/' + Design_folder_name + '/' + Design_tag_name
if os.path.exists(os.environ['workfolder_of_pt'] + '/HT_spice_work') == True :
	shutil.rmtree(os.environ['workfolder_of_pt'] + '/HT_spice_work')
os.makedirs(os.environ['workfolder_of_pt'] + '/HT_spice_work')
#############################################################################################
inserted_HT = open(os.environ['workfolder_of_pt'] + '/HT_location_database.txt','r')
inserted_HT_lines = inserted_HT.read().splitlines()
inserted_HT.close()
# malicious_file = open(os.environ['workfolder_of_pt'] + '/trojan_paths/garbel_info.txt','r')
# malicious_file_lines = malicious_file.read().splitlines()
# malicious_file.close()
# find setup values for registers:
string_slack = 'cell_name path_num slack' + '\n'
st_file = open(os.environ['workfolder_of_pt'] + '/setup_values.txt', 'r')
line_st = st_file.read().splitlines()
st_file.close()

for i in range(1,len(inserted_HT_lines)):
	inserted_HT_lines_det = (inserted_HT_lines[i]).strip().split()
	os.environ['design_name_of_pt'] = inserted_HT_lines_det[0]
	os.environ['parasitics_dir'] = os.environ['workfolder_of_pt'] + '/netlist_trojans/' + inserted_HT_lines_det[0] + '.max'
	mal_paths_new = [inserted_HT_lines_det[5],inserted_HT_lines_det[11],inserted_HT_lines_det[12],inserted_HT_lines_det[13],inserted_HT_lines_det[14]]
	os.environ['mal_paths'] = ' '.join(mal_paths_new)
	######
	os.makedirs(os.environ['workfolder_of_pt'] + '/HT_spice_work' + '/spice' + inserted_HT_lines_det[0])
	os.makedirs(os.environ['workfolder_of_pt'] + '/HT_spice_work' + '/spice' + inserted_HT_lines_det[0] + '/spice_netlist')
	os.makedirs(os.environ['workfolder_of_pt'] + '/HT_spice_work' + '/spice' + inserted_HT_lines_det[0] + '/spice_netlist/Paths')
	#############################################################################################
	#								 now extract SPICE netlists									#
	os.environ['maxvolt'] = str(V_max)
	os.environ['minvolt'] = str(V_min)
	os.environ['period_of_design'] = str(period_of_designn_1)
	os.environ['spice_folder_tcl'] = os.environ['workfolder_of_pt'] + '/HT_spice_work/spice' + inserted_HT_lines_det[0]
	#####
	subprocess.call(["pt_shell", "-f", "./02_gen_spice.tcl"])
	# check if path exist after HT insertion: note still for some TT paths we dont have the path after insertion, because the inserted trojan circuit might change the timing arcs
	# make sure to check all timing paths are constrained paths after Trojan insertion
	subprocess.call(["pt_shell", "-f", "./03_STAmachine_min.tcl"])
	#############################################################################################
	path_folder_dir = os.environ['workfolder_of_pt'] + '/HT_spice_work/spice' + inserted_HT_lines_det[0] + '/spice_netlist/Paths'
	corner_Tech = 'TT'
	V_session = ''
	V_min = '0.95'
	V_max = '0.93'
	T_period = '1.3'
	inserted_ht_cel = inserted_HT_lines_det[0]
	for wariable in mal_paths_new_new:
		setup_val = line_st[int(wariable)]
		string_slack += spice_run(path_folder_dir, wariable, corner_Tech, V_session, V_min, V_max, setup_val, T_period, inserted_ht_cel, monte_carlo_number, spf_lib_, spice_lib_) + '\n'

res = open (os.environ['workfolder_of_pt'] + '/HT_spice_work/slack_trojan.txt','w')
res.write(string_slack)
res.close()





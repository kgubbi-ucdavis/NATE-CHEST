import os
import numpy as np
import math 
import subprocess
import shutil
#############################################################################################
#					 	setting variables according to config file							#
tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)
period_of_designn = float(period)
Design_folder_name = Design_name
os.environ['clock_ports'] = clock_ports_name
os.environ['sdc_of_pt']= constraint_dir
os.environ['mw_of_pt']= milkyway_lib_dir
os.environ['design_name_of_pt']= top_name_
workfolder = RH_result_dir
os.environ['numofpaths']= num_of_paths_
os.environ['nworst_']= num_of_nworst_
os.environ['parasitic_'] = para_dir_
os.environ['target_'] = target_lib_
os.environ['scaling_lib_1'] = scaling_lib_1
os.environ['scaling_lib_2'] = scaling_lib_2
os.environ['scaling_lib_3'] = scaling_lib_3
os.environ['search_path_'] = search_path_
os.environ['period_of_design'] = str(period_of_designn)
os.environ['waveform_of_design'] = '{0 ' + str(period_of_designn/2) + '}'
os.environ['workfolder_of_pt']= '../../Designs/' + Design_folder_name + '/' + Design_tag_name
final_output_files = os.environ['workfolder_of_pt'] + '/output/'
os.environ['minvolt'] = v_min
os.environ['maxvolt'] = v_max
#############################################################################################
#							 making folders and directories:								#
if os.path.exists("../../Designs/" + Design_folder_name) == False :
	os.makedirs("../../Designs/" + Design_folder_name)
if os.path.exists(os.environ['workfolder_of_pt']) == True :
	shutil.rmtree(os.environ['workfolder_of_pt'])
os.makedirs(os.environ['workfolder_of_pt'])
os.makedirs(os.environ['workfolder_of_pt'] + "/generated_inputs")


#############################################################################################
#			using PT, we generate timing paths,												#
#			we generate info of timing-paths												#
#			we generate SPICE models, and lastly we find the GTM with IR-ATA voltages		#
subprocess.call(["pt_shell", "-f", "/home/kgubbi/STA_machine/generating_paths.tcl"])
subprocess.call(["pt_shell", "-f", "/home/kgubbi/STA_machine/STAmachine_min.tcl"])
# these two generates SPICE netlists. if you have the timing info of malicious circuit, then comment them out:
subprocess.call(["pt_shell", "-f", "/home/kgubbi/STA_machine/021_gen_spice.tcl"])
subprocess.call(["pt_shell", "-f", "/home/kgubbi/STA_machine/022_gen_spice.tcl"])
# this finds the GTM of IR-ATA:
subprocess.call(["pt_shell", "-f", "/home/kgubbi/STA_machine/GTM_IRATA.tcl"])
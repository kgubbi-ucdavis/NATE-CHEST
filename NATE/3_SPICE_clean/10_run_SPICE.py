import os
import subprocess
import shutil
from shutil import copyfile
############################################################
########				variables					########
############################################################
Design_folder_name = os.environ['Design_folder']
Design_tag_name = os.environ['tag_name']
T_period = float(os.environ['period_of_design'])
spf_lib_ = os.environ['spf_lib_']
spice_lib_ = os.environ['spice_lib_']
monte_carlo_number = os.environ['monte_carlo_number']
########################################################################################################
########									Generate netlist									########
########################################################################################################
os.environ['workfolder_of_pt'] = '../../Designs/' + Design_folder_name + '/' + Design_tag_name
os.environ['spice_folder_tcl'] = os.environ['workfolder_of_pt'] + '/spice'
path_folder_dir = os.environ['workfolder_of_pt'] + '/spice/spice_netlist/Paths'
path_number_real_file = open(os.environ['workfolder_of_pt'] + '/generated_inputs/num_of_paths/num_of_paths.txt', 'r')
path_number_real = path_number_real_file.read().splitlines()
path_number_real_file.close()
os.environ['num_paths']= str(path_number_real[0])
########################################################################################################
########################################################################################################
# reading setup time:
st_file = open(os.environ['workfolder_of_pt'] + '/setup_values.txt', 'r')
line_st = st_file.read().splitlines()
st_file.close()
####################
string_for_slack = 'Path_number   Slack_for_V_AVATAR(ps)' + '\n'
for variab_ in range(int(os.environ['lower_range']), int(os.environ['upper_range'])):
	print 'path number is ' + str(variab_)
	if os.path.exists(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR') == True :
		shutil.rmtree(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR')
	os.makedirs(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR')
	########################################################################################################
	# note for monte carlo, template inside .SPO file should be:
	# GAUSS(nominal_val, rel_variation, num_sigmas [, multiplier])
	# .PARAM vth_pmos_pv=GAUSS(-0.3021,0.1,1)
	# after revising the library to contain the gaussian distribution (like above line), then uncomment this:
	# start of MONTE : >>>
#	stri = ''
#	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_stim.spo', 'r')
#	lines = tmp.read().splitlines()
#	l = len(lines)
#	for i in range(l):
#		if lines[i] == '* Start: Victim Measure Statements':
#			start_stim = i
#		if lines[i] == '* End: Victim Measure Statements':
#			end_stim =i
#		if (lines[i]).startswith('.tran'):
#			line_analysis = (lines[i]).strip().split()
#			lines[i] = line_analysis[0] + ' ' + line_analysis[1] + ' ' + line_analysis[2] + ' SWEEP MONTE=' + str(monte_carlo_number)
#	stim_string = '\n'.join(lines)
#	tmp.close()
#	os.remove(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_stim.spo')
#	Results = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_stim.spo', 'w')
#	Results.write(stim_string)
#	Results.close()
#	######## fix for capture path
#	stri = ''	
#	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_stim.spo', 'r')
#	lines = tmp.read().splitlines()
#	l = len(lines)
#	for i in range(l):
#		if lines[i] == '* Start: Victim Measure Statements':
#			start_stim = i
#		if lines[i] == '* End: Victim Measure Statements':
#			end_stim =i
#		if (lines[i]).startswith('.tran'):
#			line_analysis = (lines[i]).strip().split()
#			lines[i] = line_analysis[0] + ' ' + line_analysis[1] + ' ' + line_analysis[2] + ' SWEEP MONTE=' + str(monte_carlo_number)
#	stim_string = '\n'.join(lines)
#	tmp.close()
#	os.remove(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_stim.spo')
#	Results = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_stim.spo', 'w')
#	Results.write(stim_string)
#	Results.close()
	# end of MONTE : <<<
	########################################################################################################
	########										fix plus										########
	# sometimes the version of SPICE is not compatible with what PrimeTime generates.
	# here I revised the SPICE netlist to remove linebreaks 
	stri = ''
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_fixed_plus.spo', 'w')
	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path.spo', 'r')
	lines = tmp.read().splitlines()
	l = len(lines)
	for i in range(l-1):
		line_items_i = lines[i]
		line_items_i1 = lines[i+1]
		if line_items_i1.startswith('+'):
			line_continuous = line_items_i1.strip().split()
			lc = len(line_continuous)
			line_c =[None]*(lc-1)
			for k in range(1,lc):
				line_c[k-1] = line_continuous[k]
			line_c = ' '.join(line_c)
			
			stri +=  lines[i] + ' ' + line_c + '\n'
		elif line_items_i.startswith('+'):
			pass
		else:
			stri += lines[i] +'\n'
	Results.write(stri)
	Results.close()
	tmp.close()
	######## fix plus for capture path
	stri = ''
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_fixed_plus.spo', 'w')
	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path.spo', 'r')
	lines = tmp.read().splitlines()
	l = len(lines)
	for i in range(l-1):
		line_items_i = lines[i]
		line_items_i1 = lines[i+1]
		if line_items_i1.startswith('+'):
			line_continuous = line_items_i1.strip().split()
			lc = len(line_continuous)
			line_c =[None]*(lc-1)
			for k in range(1,lc):
				line_c[k-1] = line_continuous[k]
			line_c = ' '.join(line_c)
			
			stri +=  lines[i] + ' ' + line_c + '\n'
		elif line_items_i.startswith('+'):
			pass
		else:
			stri += lines[i] +'\n'
	Results.write(stri)
	Results.close()
	tmp.close()	
	########################################################################################################
	########										fix pins										########
	# some SPICE versions generated errors, saying the variable declaration is wrong because there exist a "." in the variable name
	# here I remove the "."
	# also I corrected the directory of libraries
	# note that we don't have a header file to generate a good SPICE netlist from PrimeTime. So the pin order is messed up.
	# you need to revise the library and fix the pin ordering, or find a header file. check spice_deck manual page in PrimeTime.
	stri = '#path' + '\n'
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/path.spo', 'w')
	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_fixed_plus.spo', 'r')
	lines = tmp.read().splitlines()
	l = len(lines)
	lines.extend([''])
	for i in range(l):
		lines[i] = lines[i].replace(".VDD","VDD")
		line_items_i = lines[i]
		lines[i+1] = lines[i+1].replace(".VDD","VDD")
		line_items_i1 = lines[i+1]
		if line_items_i.startswith('.include'):
			lines[i] = '.prot' + '\n' \
			+ '.include ' + spf_lib_ + '\n' \
			+ '.lib ' + spice_lib_ + ' TT' + '\n' \
			+ '.unprot' + '\n' \
			+ '.include "' + path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/path_stim.spo"'
		if line_items_i.startswith('x'):
			line_c = line_items_i.strip().split()
			line_c1 = line_items_i1.strip().split()
			li = len(line_c)
			li1 = len(line_c1)
			line_c.extend([None,None])
			line_c[li+1] = line_c[li-1]
			line_c[li-1] = line_c1[2]
			line_c[li] = line_c1[1]
			line_c = ' '.join(line_c)	
			lines[i] = line_c
		stri += lines[i] + '\n'
	Results.write(stri)
	Results.close()
	tmp.close()
	######## fix pins for capture path
	stri = '#path' + '\n'
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/path.spo', 'w')
	tmp = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_fixed_plus.spo', 'r')
	lines = tmp.read().splitlines()
	l = len(lines)
	lines.extend([''])
	for i in range(l):
		lines[i] = lines[i].replace(".VDD","VDD")
		line_items_i = lines[i]
		lines[i+1] = lines[i+1].replace(".VDD","VDD")
		line_items_i1 = lines[i+1]
		if line_items_i.startswith('.include'):
			lines[i] = '.prot' + '\n' \
			+ '.include ' + spf_lib_ + '\n' \
			+ '.lib ' + spice_lib_ + ' TT' + '\n' \
			+ '.unprot' + '\n' \
			+ '.include "' + path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/inputs/path_stim.spo"'
		if line_items_i.startswith('x'):
			line_c = line_items_i.strip().split()
			line_c1 = line_items_i1.strip().split()
			li = len(line_c)
			li1 = len(line_c1)
			line_c.extend([None,None])
			line_c[li+1] = line_c[li-1]
			line_c[li-1] = line_c1[2]
			line_c[li] = line_c1[1]
			line_c = ' '.join(line_c)	
			lines[i] = line_c
		stri += lines[i] + '\n'
	Results.write(stri)
	Results.close()
	tmp.close()	
	########################################################################
	os.makedirs(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/for_capture/')
	########################################################################
	########		   copy the .spo and keep the original	  		########
	######################################################################## 
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/path.spo', 'w')
	tmp1 = open(path_folder_dir + '/Path' + str(variab_) + '/path.spo', 'r')
	lines = tmp1.read().splitlines()
	stri = '\n'.join(lines)		
	Results.write(stri)
	Results.close()
	tmp1.close() 
	######## for capture path
	Results = open(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/for_capture/path.spo', 'w')
	tmp1 = open(path_folder_dir + '/Path' + str(variab_) + '/generated_inputs/Capture_calculations/path.spo', 'r')
	lines = tmp1.read().splitlines()
	stri = '\n'.join(lines)		
	Results.write(stri)
	Results.close()
	tmp1.close() 		
	###################################################################
	########				running HSPICE for 			       ########
	###################################################################
	subprocess.call(["hspice", "-i", path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/path.spo', "-o", path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/'])		
	subprocess.call(["hspice", "-i", path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/for_capture/path.spo', "-o", path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/for_capture/'])
	########################################################################
	########		 	  measurement statements		 	 		########
	########################################################################
	results_Vconv = open(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/delay_info.txt', 'w')
	tmp_lis_Vconv = open(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/path.lis', 'r')
	tmp_lis_Vconv_cap = open(path_folder_dir + '/Path' + str(variab_) + '/spice_VAVATAR/for_capture/path.lis', 'r')
	lines_lis_Vconv_cap = tmp_lis_Vconv_cap.read().splitlines()
	lines_lis_Vconv = tmp_lis_Vconv.read().splitlines()
	l_of_lines_lis_Vconv_cap = len(lines_lis_Vconv_cap)
	l_of_lines_lis_Vconv = len(lines_lis_Vconv)		
	tmp_l = open (os.environ['workfolder_of_pt'] + '/Paths/Path' + str(variab_) + '/launch/generated_inputs/delay_info_min.txt', 'r')
	tmp_c = open (os.environ['workfolder_of_pt'] + '/Paths/Path' + str(variab_) + '/capture/generated_inputs/delay_info_min.txt', 'r')
	lines_l = tmp_l.read().splitlines()
	lines_c = tmp_c.read().splitlines()
	Cell_l = lines_l[0]
	Cell_c = lines_c[0]
	Cell_d = lines_l[4]
	Cell_l = Cell_l.replace("{","")
	Cell_l = Cell_l.replace("}","")
	Cell_l = Cell_l.replace('"','')
	Cell_l = Cell_l.strip().split(' ')		
	Cell_c = Cell_c.replace("{","")
	Cell_c = Cell_c.replace("}","")
	Cell_c = Cell_c.replace('"','')
	Cell_c = Cell_c.strip().split(' ')			
	Cell_d = Cell_d.replace("{","")
	Cell_d = Cell_d.replace("}","")
	Cell_d = Cell_d.replace('"','')
	Cell_d = Cell_d.strip().split(' ')
	l_of_L = len(Cell_l)-1
	l_of_D = len(Cell_d)-1
	l_of_C = len(Cell_c)-1
	lines_l_risefall = lines_l[1]
	lines_d_risefall = lines_l[5]
	lines_c_risefall = lines_c[1]
	lines_l_risefall = lines_l_risefall.strip().split()
	lines_d_risefall = lines_d_risefall.strip().split()
	lines_c_risefall = lines_c_risefall.strip().split()			
	measure_LD = []
	measure_C = []
	stri = ''
	delay_for_LD = float(0)
	delay_for_C = float(0)
	for i in range (l_of_L):
		measure_LD.append (('delay' + '_' + Cell_l[i] + '_' + Cell_l[i+1]).upper())
	for i in range (l_of_D):
		measure_LD.append (('delay' + '_' + Cell_d[i] + '_' + Cell_d[i+1]).upper())
	for i in range (l_of_C):
		measure_C.append (('delay' + '_' + Cell_c[i] + '_' + Cell_c[i+1]).upper())
	for i in range (l_of_lines_lis_Vconv):
		(lines_lis_Vconv[i]) = (lines_lis_Vconv[i]).replace('=',' ')
		lines_lis_Vconv_detail = (lines_lis_Vconv[i]).strip().split()
		if lines_lis_Vconv_detail != []:
			lines_lis_Vconv_detail[0] = (lines_lis_Vconv_detail[0]).upper()
			if (lines_lis_Vconv_detail[0]) in measure_LD:
				stri += (lines_lis_Vconv[i]) +'\n'
				lines_lis_Vconv_detail[1] = (lines_lis_Vconv_detail[1]).replace('n','e-9')
				lines_lis_Vconv_detail[1] = (lines_lis_Vconv_detail[1]).replace('p','e-12')
				lines_lis_Vconv_detail[1] = (lines_lis_Vconv_detail[1]).replace('f','e-15')	
				lines_lis_Vconv_detail[1] = (lines_lis_Vconv_detail[1]).replace('a','e-18')	
				delay_for_LD += float((lines_lis_Vconv_detail[1]))
	delay_for_LD_Vconv_list = delay_for_LD
	for i in range (l_of_lines_lis_Vconv_cap):
		(lines_lis_Vconv_cap[i]) = (lines_lis_Vconv_cap[i]).replace('=',' ')
		lines_lis_Vconv_cap_detail = (lines_lis_Vconv_cap[i]).strip().split()
		if lines_lis_Vconv_cap_detail != []:
			lines_lis_Vconv_cap_detail[0] = (lines_lis_Vconv_cap_detail[0]).upper()
			if (lines_lis_Vconv_cap_detail[0]) in measure_C:
				stri += (lines_lis_Vconv_cap[i]) +'\n'
				lines_lis_Vconv_cap_detail[1] = (lines_lis_Vconv_cap_detail[1]).replace('n','e-9')
				lines_lis_Vconv_cap_detail[1] = (lines_lis_Vconv_cap_detail[1]).replace('p','e-12')
				lines_lis_Vconv_cap_detail[1] = (lines_lis_Vconv_cap_detail[1]).replace('f','e-15')	
				lines_lis_Vconv_cap_detail[1] = (lines_lis_Vconv_cap_detail[1]).replace('a','e-18')	
				delay_for_C += float((lines_lis_Vconv_cap_detail[1]))
	delay_for_C_Vconv_list = delay_for_C
	results_Vconv.write(stri)
	results_Vconv.close()
	delay_for_LD = float(0)
	delay_for_C = float(0)
	warwar = variab_ - 0
	Slack_Vconv = (delay_for_C_Vconv_list - (float(line_st[warwar])*(1e-9)) + T_period - delay_for_LD_Vconv_list)*(1e12)
	string_for_slack += str(variab_) + '   ' + str(Slack_Vconv) + '\n'
	tmp_l.close()
	tmp_c.close()
	tmp_lis_Vconv.close()
	tmp_lis_Vconv_cap.close()
	########################################################################
	########	   Slack calculation based on spice model		  	########
	########################################################################
tmp_slack_results = open(os.environ['workfolder_of_pt'] + '/spice/' + str(os.environ['output_iter']) + '_Slacks.txt', 'w')			
tmp_slack_results.write(string_for_slack)
tmp_slack_results.close()


import os
import subprocess
import shutil
import glob
import time
###################################################################
tmp = open('./config.txt', 'r')
tmp_ = tmp.read()
tmp.close()
eval(tmp_)
###################################################################################################
design_directory = '../../Designs/' + Design_folder_name + '/' + Design_tag_name
path_number_real_file = open(design_directory + '/generated_inputs/num_of_paths/num_of_paths.txt', 'r')
path_number_real = path_number_real_file.read().splitlines()
path_number_real_file.close()
num_runs = int(path_number_real[0])
####
if os.path.exists("./spice_sbatch_files" + Design_folder_name) == True :
	shutil.rmtree("./spice_sbatch_files" + Design_folder_name)
os.makedirs("./spice_sbatch_files" + Design_folder_name)
####
for filename in glob.glob(design_directory + '/spice/*Slacks.txt'):
	os.remove(filename)
for filename in glob.glob('./log/SPICE_log' + Design_folder_name + '*'):
	os.remove(filename)
####
iteratns = int(num_runs/num_spice_each_run)
for i in range(iteratns):
	low_range = i*num_spice_each_run
	up_range = ((i+1)*num_spice_each_run)
	
	stri = \
	"#!/usr/bin/env sh" + '\n' + \
	"" + '\n' + \
	"#SBATCH --job-name make" + '\n' + \
	"#SBATCH --qos=hhqos" + '\n' + \
	"#SBATCH --partition=HH_q" + '\n' + \
	"#SBATCH --nodes 1" + '\n' + \
	"#SBATCH --time=4-1:00" + '\n' + \
	"##SBATCH --ntasks-per-node 1" + '\n' + \
	"##SBATCH --gres=gpu:1" + '\n' + \
	"#SBATCH --output=./log/SPICE_log_" + Design_folder_name + str(i) + ".log" + '\n' + \
	"" + '\n' + \
	"##SBATCH --mem 2G" + '\n' + \
	"" + '\n' + \
	"module load synopsys/hspice/N-2017.12-SP1" + '\n' + \
	"export period_of_design=" + str(period_of_design) + '\n' + \
	"export Design_folder=" + str(Design_folder_name) + '\n' + \
	"export spf_lib_=" + str(spf_lib_) + '\n' + \
	"export spice_lib_=" + str(spice_lib_) + '\n' + \
	"export tag_name=" + str(Design_tag_name) + '\n' + \
	"export monte_carlo_number=" + str(monte_carlo_number) + '\n' + \
	"export lower_range=" + str(low_range) + '\n' + \
	"export upper_range=" + str(up_range) + '\n' + \
	"export output_iter=" + str(i) + '\n' + \
	"setenv META_QUEUE 1" + '\n' + \
	"export META_QUEUE=1" + '\n' + \
	"python ./10_run_SPICE.py" + '\n' + \
	"" + '\n' + \
	"" + '\n' + \
	"module unload synopsys/hspice/N-2017.12-SP1" + '\n'


	tmp_file = open('./tmp.sh', 'w')
	tmp_file.write(stri)
	tmp_file.close()
	tmp_file = open('./spice_sbatch_files' + Design_folder_name + '/tmp' + str(i) + '.sh', 'w')
	tmp_file.write(stri)
	tmp_file.close()
	
	subprocess.check_output(['sbatch', './tmp.sh'])
	os.remove('./tmp.sh')

if (num_runs % num_spice_each_run != 0):
	low_range = iteratns*num_spice_each_run
	up_range = num_runs
	i = iteratns
	stri = \
	"#!/usr/bin/env sh" + '\n' + \
	"" + '\n' + \
	"#SBATCH --job-name make" + '\n' + \
	"#SBATCH --qos=hhqos" + '\n' + \
	"#SBATCH --partition=all-LoPri" + '\n' + \
	"#SBATCH --nodes 1" + '\n' + \
	"#SBATCH --time=4-1:00" + '\n' + \
	"##SBATCH --ntasks-per-node 1" + '\n' + \
	"##SBATCH --gres=gpu:1" + '\n' + \
	"#SBATCH --output=./log/SPICE_log_" + Design_folder_name + str(i) + ".log" + '\n' + \
	"" + '\n' + \
	"##SBATCH --mem 2G" + '\n' + \
	"" + '\n' + \
	"module load synopsys/hspice/N-2017.12-SP1" + '\n' + \
	"export period_of_design=" + str(period_of_design) + '\n' + \
	"export Design_folder=" + str(Design_folder_name) + '\n' + \
	"export spf_lib_=" + str(spf_lib_) + '\n' + \
	"export spice_lib_=" + str(spice_lib_) + '\n' + \
	"export tag_name=" + str(Design_tag_name) + '\n' + \
	"export monte_carlo_number=" + str(monte_carlo_number) + '\n' + \
	"export lower_range=" + str(low_range) + '\n' + \
	"export upper_range=" + str(up_range) + '\n' + \
	"export output_iter=" + str(i) + '\n' + \
	"setenv META_QUEUE 1" + '\n' + \
	"export META_QUEUE=1" + '\n' + \
	"python ./10_run_SPICE.py" + '\n' + \
	"" + '\n' + \
	"" + '\n' + \
	"module unload synopsys/hspice/N-2017.12-SP1" + '\n'


	tmp_file = open('./tmp.sh', 'w')
	tmp_file.write(stri)
	tmp_file.close()
	tmp_file = open('./spice_sbatch_files' + Design_folder_name + '/tmp' + str(i) + '.sh', 'w')
	tmp_file.write(stri)
	tmp_file.close()
	
	subprocess.check_output(['sbatch', './tmp.sh'])
	os.remove('./tmp.sh')

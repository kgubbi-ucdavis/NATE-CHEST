#module add synopsys/primetime/K-2015.12-SP1
#pt_shell
# #######################################
# #######################################
# ####	revise these:
set spice_folder $env(spice_folder_tcl)
set workfolder $env(workfolder_of_pt)
cd $env(mw_of_pt)
cd ../
set DESIGN_NAME $env(design_name_of_pt)
set SDC_FILE $env(sdc_of_pt)
set ADDITIONAL_SEARCH_PATH $env(search_path_)
set_app_var search_path ". ${ADDITIONAL_SEARCH_PATH} $search_path"
set TARGET_LIBRARY_FILES $env(target_lib_)
set_app_var target_library ${TARGET_LIBRARY_FILES}
set_app_var link_library "* $target_library"
read_milkyway -library  $env(mw_of_pt) $env(design_name_of_pt)
source ${SDC_FILE}
# #######################################
# #######################################
create_clock [get_ports $env(clock_ports)]  -name clktop  -period $env(period_of_design)
set_clock_uncertainty 0 [get_clocks clktop]
# first group all paths from reg to reg:
group_path -name input_paths -from [get_ports * -filter "direction==in"]
group_path -name output_paths -to [get_ports * -filter "direction==out"]

set_rail_voltage -min -rail_value $env(minvolt) [get_cells *]
set_rail_voltage -max -rail_value $env(maxvolt) [get_cells *]

# #######################################
# procedure to generate SPICE models
proc spice_generator_proc {path_counter spice_folder workfolder} {
	set path_list [regexp -inline -all -- {\S+} $path_counter]
	foreach x $path_list {
		echo "path is ${x}"
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}	
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs
		source ${workfolder}/Paths/Path${x}/the_path_origin.txt
		# report_timing -pba_mode path -path_type full_clock_expanded $my_path
		source ${workfolder}/Paths/Path${x}/the_path_origin_for_capture.txt
		# report_timing -pba_mode path -path_type full_clock_expanded $my_path_capture
		write_spice_deck -output ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/path.spo $my_path
		write_spice_deck -output ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/path.spo $my_path_capture
	}

}

# #######################################
# #######################################
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitics_dir)
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitics_dir)
set malic_paths $env(mal_paths)
spice_generator_proc $malic_paths $spice_folder $workfolder
# #######################################
exit

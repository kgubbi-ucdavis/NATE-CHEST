#module add synopsys/primetime/K-2015.12-SP1
#pt_shell
# #######################################
# #######################################
# ####	revise these:
set workfolder $env(workfolder_of_pt)
set spice_folder $env(spice_folder_tcl)
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
define_scaling_lib_group {
$env(scaling_lib_1)
$env(scaling_lib_2)
$env(scaling_lib_3)
}

set_rail_voltage -min -rail_value $env(minvolt) [get_cells *]
set_rail_voltage -max -rail_value $env(maxvolt) [get_cells *]


report_timing
remove_annotated_parasitics
read_parasitics $env(parasitics_dir)
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitics_dir)
set path_list [regexp -inline -all -- {\S+} $env(mal_paths)]
foreach x $path_list {
	source ${workfolder}/Paths/Path${x}/the_path_origin.txt
	report_timing $my_path -voltage
	# writing launch info		
	get_attribute [get_attribute [get_attribute [get_attribute $my_path launch_clock_paths] points] object] full_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute $my_path launch_clock_paths] points] rise_fall >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute $my_path launch_clock_paths] points] arrival >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_cells -of_objects [get_attribute [get_attribute [get_attribute $my_path launch_clock_paths] points] object ]] ref_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	# writing data info
	get_attribute [get_attribute [get_attribute $my_path points] object] full_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_attribute $my_path points] rise_fall >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_attribute $my_path points] arrival >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_cells -of_objects [get_attribute [get_attribute $my_path points] object ]] ref_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	# cell names for spice use
	get_attribute [get_attribute [get_attribute [get_attribute [get_attribute $my_path launch_clock_paths] points] object] cell] full_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute [get_attribute $my_path points] object] cell] full_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/delay_info_min.txt
	# writing capture info
	get_attribute [get_attribute [get_attribute [get_attribute $my_path capture_clock_paths] points] object] full_name  >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute $my_path capture_clock_paths] points] rise_fall >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute $my_path capture_clock_paths] points] arrival >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/delay_info_min.txt
	get_attribute [get_cells -of_objects [get_attribute [get_attribute [get_attribute $my_path capture_clock_paths] points] object ]] ref_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/delay_info_min.txt
	get_attribute [get_attribute [get_attribute [get_attribute [get_attribute $my_path capture_clock_paths] points] object] cell] full_name >> ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs/delay_info_min.txt
}

exit
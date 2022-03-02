# #######################################
# ####	revise these:
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
create_clock [get_ports $env(clock_ports)]  -name clktop  -period $env(period_of_design)
set_clock_uncertainty  $env(uncert) [get_clocks clktop]
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
read_parasitics $env(parasitic_)
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitic_)

set fp [open "${workfolder}/generated_inputs/num_of_paths/num_of_paths.txt" r]
set number_of_files [read $fp]
close $fp

for {set x 0} {$x<$number_of_files} {incr x} {
	source ${workfolder}/Paths/Path${x}/the_path_origin.txt
	report_timing $my_path -voltage >> ${workfolder}/Paths/Path${x}/IR_ATA_timing_report.txt
	get_attribute $my_path slack >> ${workfolder}/GTM_slacks_IR_ATA.txt
	get_attribute [get_timing_paths $my_path -pba_mode path] endpoint_setup_time_value >> ${workfolder}/setup_values.txt
}

exit
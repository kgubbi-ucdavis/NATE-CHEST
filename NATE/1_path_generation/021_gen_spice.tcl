# #######################################
# ####	revise these:
set spice_folder $env(workfolder_of_pt)/spice
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

file mkdir ${spice_folder}
file mkdir ${spice_folder}/spice_netlist
file mkdir ${spice_folder}/spice_netlist/Paths

set_rail_voltage -min -rail_value $env(maxvolt) [get_cells *]
set_rail_voltage -max -rail_value $env(maxvolt) [get_cells *]

# #######################################
# procedure to generate SPICE models
proc spice_generator_proc {path_counter spice_folder workfolder} {
	for {set x 0} {$x<[expr $path_counter]} {incr x} {
		echo "path is ${x}"
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}	
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations
		file mkdir ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/Capture_calculations/inputs
		source ${workfolder}/Paths/Path${x}/the_path_origin.txt
		write_spice_deck -output ${spice_folder}/spice_netlist/Paths/Path${x}/generated_inputs/path.spo $my_path
	}

}

# #######################################
# #######################################
set fp [open "${workfolder}/generated_inputs/num_of_paths/num_of_paths.txt" r]
set path_counter [read $fp]
close $fp
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitic_)
report_timing
remove_annotated_parasitics
read_parasitics $env(parasitic_)

spice_generator_proc $path_counter $spice_folder $workfolder
# #######################################
exit

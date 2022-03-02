# #######################################
# ####	revise these:
source ./config.tcl
set workfolder "../../Designs/${Design_name}/${Design_tag_name}"
set spice_folder "${workfolder}/NN_training_PT"
cd "${milkyway_lib_dir}"
cd ../
set ADDITIONAL_SEARCH_PATH "${search_path_}"
set_app_var search_path ". ${ADDITIONAL_SEARCH_PATH} $search_path"
set TARGET_LIBRARY_FILES "${target_lib_}"
set_app_var target_library ${TARGET_LIBRARY_FILES}
set_app_var link_library "* $target_library"
read_milkyway -library  ${milkyway_lib_dir} ${top_name_}
source ${constraint_dir}

if {[file isdirectory ${spice_folder}]} {
	file delete -force -- ${spice_folder}
}
file mkdir ${spice_folder}
# #######################################
create_clock [get_ports ${clock_ports_name}]  -name clktop  -period ${period_}
set_clock_uncertainty 0 [get_clocks clktop]
set libb []
lappend libb ${scaling_lib_1}
lappend libb ${scaling_lib_2}
lappend libb ${scaling_lib_3}
define_scaling_lib_group $libb

set_rail_voltage -min -rail_value $minvolt_ [get_cells *]
set_rail_voltage -max -rail_value $maxvolt_ [get_cells *]

report_timing
remove_annotated_parasitics
read_parasitics "${para_dir_}"
report_timing
remove_annotated_parasitics
read_parasitics "${para_dir_}"

set fp [open "${workfolder}/generated_inputs/num_of_paths/num_of_paths.txt" r]
set number_of_files [read $fp]
close $fp
# #######################################
for {set i 0} {$i<$number_of_files} {incr i} {
	echo $i
	source ${workfolder}/Paths/Path${i}/the_path_origin.txt
	get_attribute [get_timing_paths $my_path -pba_mode path] endpoint_setup_time_value >> ${spice_folder}/setup_pt.txt
	get_attribute $my_path slack >> ${spice_folder}/slack_pt.txt
# ############################################################################################################################################################
# for number of cells in different paths & strength >>> :
	set cap_file [open "${workfolder}/Paths/Path${i}/capture/generated_inputs/delay_info_min.txt" r]
	set cap_file_detail [read $cap_file]
	close $cap_file
	set cap_line [split $cap_file_detail "\n"]
	set cap_cels [split [lindex $cap_line 0] " "]
	set num_of_cels [llength $cap_cels]
	set capture_cel_list []
	
	set lan_file [open "${workfolder}/Paths/Path${i}/launch/generated_inputs/delay_info_min.txt" r]
	set lan_file_detail [read $lan_file]
	close $lan_file
	set lan_line [split $lan_file_detail "\n"]
	set lan_cels [split [lindex $lan_line 0] " "]
	set lan_num_of_cels [llength $lan_cels]
	set launch_cel_list []
	
	set dat_cels [split [lindex $lan_line 4] " "]
	set dat_num_of_cels [llength $dat_cels]
	set data_cel_list []
	#capture + common:
	for {set y 0} {$y<$num_of_cels} {incr y} {
		if {[lindex $cap_cels ${y}] != $env(clock_ports)} {
			lappend capture_cel_list [get_attribute [get_cells -of_objects [lindex $cap_cels ${y}]] full_name]
		}
		# if {[expr $y%2]==1} {
			# puts -nonewline $net_area_file "[lindex $cap_cels ${y}] [get_attribute [get_nets -of_objects [lindex $cap_cels ${y}]] area] "
		# }
	}
	set cap_cel_list [lsort -unique $capture_cel_list]
	# launch + common:
	for {set y 0} {$y<$lan_num_of_cels} {incr y} {
		if {[lindex $lan_cels ${y}] != $env(clock_ports)} {
			lappend launch_cel_list [get_attribute [get_cells -of_objects [lindex $lan_cels ${y}]] full_name]
		}
	}
	set lan_cel_list [lsort -unique $launch_cel_list]
	# data:
	for {set y 0} {$y<$dat_num_of_cels} {incr y} {
		if {[lindex $dat_cels ${y}] != $env(clock_ports)} {
			lappend data_cel_list [get_attribute [get_cells -of_objects [lindex $dat_cels ${y}]] full_name]
		}
	}
	set dat_cel_list [lsort -unique $data_cel_list]
	# common:
	set com_cel_list []
	for {set y 0} {$y<[llength $cap_cel_list]} {incr y} {
		if {[lsearch -exact $launch_cel_list [lindex $cap_cel_list ${y}]] >= 0} {
			lappend com_cel_list [lindex $cap_cel_list ${y}]
		}
	}
	# capture - common & launch - common:
	for {set y 0} {$y<[llength $com_cel_list]} {incr y} {
		set idx [lsearch $cap_cel_list [lindex $com_cel_list ${y}]]
		set cap_cel_list [lreplace $cap_cel_list $idx $idx]
		
		set idx [lsearch $lan_cel_list [lindex $com_cel_list ${y}]]
		set lan_cel_list [lreplace $lan_cel_list $idx $idx]
	}
	# now strength of capture:
	set x0 0
	set x1 0
	set x2 0
	set x4 0
	set x8 0
	set x16 0
	set x32 0
	for {set y 0} {$y<[llength $cap_cel_list]} {incr y} {
		if {[string first "X0" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x0 [expr $x0 +1]
		}
		if {[string first "X1" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x1 [expr $x1 +1]
		}		
		if {[string first "X2" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x2 [expr $x2 +1]
		}		
		if {[string first "X4" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x4 [expr $x4 +1]
		}		
		if {[string first "X8" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x8 [expr $x8 +1]
		}		
		if {[string first "X16" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x16 [expr $x16 +1]
		}		
		if {[string first "X32" [get_attribute [get_cells [lindex $cap_cel_list ${y}]] ref_name]] != -1} {
			set x32 [expr $x32 +1]
		}
	}
	echo $x0 >> ${spice_folder}/strength_x0_capture_pt.txt
	echo $x1 >> ${spice_folder}/strength_x1_capture_pt.txt
	echo $x2 >> ${spice_folder}/strength_x2_capture_pt.txt
	echo $x4 >> ${spice_folder}/strength_x4_capture_pt.txt
	echo $x8 >> ${spice_folder}/strength_x8_capture_pt.txt
	echo $x16 >> ${spice_folder}/strength_x16_capture_pt.txt
	echo $x32 >> ${spice_folder}/strength_x32_capture_pt.txt
	# now strength of launch:
	set x0 0
	set x1 0
	set x2 0
	set x4 0
	set x8 0
	set x16 0
	set x32 0
	for {set y 0} {$y<[llength $lan_cel_list]} {incr y} {
		if {[string first "X0" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x0 [expr $x0 +1]
		}
		if {[string first "X1" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x1 [expr $x1 +1]
		}		
		if {[string first "X2" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x2 [expr $x2 +1]
		}		
		if {[string first "X4" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x4 [expr $x4 +1]
		}		
		if {[string first "X8" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x8 [expr $x8 +1]
		}		
		if {[string first "X16" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x16 [expr $x16 +1]
		}		
		if {[string first "X32" [get_attribute [get_cells [lindex $lan_cel_list ${y}]] ref_name]] != -1} {
			set x32 [expr $x32 +1]
		}
	}
	echo $x0 >> ${spice_folder}/strength_x0_launch_pt.txt
	echo $x1 >> ${spice_folder}/strength_x1_launch_pt.txt
	echo $x2 >> ${spice_folder}/strength_x2_launch_pt.txt
	echo $x4 >> ${spice_folder}/strength_x4_launch_pt.txt
	echo $x8 >> ${spice_folder}/strength_x8_launch_pt.txt
	echo $x16 >> ${spice_folder}/strength_x16_launch_pt.txt
	echo $x32 >> ${spice_folder}/strength_x32_launch_pt.txt
	# now strength of data:
	set x0 0
	set x1 0
	set x2 0
	set x4 0
	set x8 0
	set x16 0
	set x32 0
	for {set y 0} {$y<[llength $dat_cel_list]} {incr y} {
		if {[string first "X0" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x0 [expr $x0 +1]
		}
		if {[string first "X1" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x1 [expr $x1 +1]
		}		
		if {[string first "X2" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x2 [expr $x2 +1]
		}		
		if {[string first "X4" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x4 [expr $x4 +1]
		}		
		if {[string first "X8" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x8 [expr $x8 +1]
		}		
		if {[string first "X16" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x16 [expr $x16 +1]
		}		
		if {[string first "X32" [get_attribute [get_cells [lindex $dat_cel_list ${y}]] ref_name]] != -1} {
			set x32 [expr $x32 +1]
		}
	}
	echo $x0 >> ${spice_folder}/strength_x0_data_pt.txt
	echo $x1 >> ${spice_folder}/strength_x1_data_pt.txt
	echo $x2 >> ${spice_folder}/strength_x2_data_pt.txt
	echo $x4 >> ${spice_folder}/strength_x4_data_pt.txt
	echo $x8 >> ${spice_folder}/strength_x8_data_pt.txt
	echo $x16 >> ${spice_folder}/strength_x16_data_pt.txt
	echo $x32 >> ${spice_folder}/strength_x32_data_pt.txt
	# now strength of common:
	set x0 0
	set x1 0
	set x2 0
	set x4 0
	set x8 0
	set x16 0
	set x32 0
	for {set y 0} {$y<[llength $com_cel_list]} {incr y} {
		if {[string first "X0" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x0 [expr $x0 +1]
		}
		if {[string first "X1" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x1 [expr $x1 +1]
		}		
		if {[string first "X2" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x2 [expr $x2 +1]
		}		
		if {[string first "X4" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x4 [expr $x4 +1]
		}		
		if {[string first "X8" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x8 [expr $x8 +1]
		}		
		if {[string first "X16" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x16 [expr $x16 +1]
		}		
		if {[string first "X32" [get_attribute [get_cells [lindex $com_cel_list ${y}]] ref_name]] != -1} {
			set x32 [expr $x32 +1]
		}
	}
	echo $x0 >> ${spice_folder}/strength_x0_common_pt.txt
	echo $x1 >> ${spice_folder}/strength_x1_common_pt.txt
	echo $x2 >> ${spice_folder}/strength_x2_common_pt.txt
	echo $x4 >> ${spice_folder}/strength_x4_common_pt.txt
	echo $x8 >> ${spice_folder}/strength_x8_common_pt.txt
	echo $x16 >> ${spice_folder}/strength_x16_common_pt.txt
	echo $x32 >> ${spice_folder}/strength_x32_common_pt.txt
	
	echo [llength $com_cel_list] >> ${spice_folder}/num_common_pt.txt
	echo [expr [llength $lan_cel_list]-0] >> ${spice_folder}/num_launch_pt.txt
	echo [expr [llength $cap_cel_list]-0] >> ${spice_folder}/num_capture_pt.txt
	echo [expr [llength $dat_cel_list]+1] >> ${spice_folder}/num_data_pt.txt
# <<< for number of cells in different paths & strength
	# launch slack:
	get_attribute [get_attribute [get_timing_paths $my_path -pba_mode path] launch_clock_paths] arrival >> ${spice_folder}/slack_launch_pt.txt
	# data slack:
	set tmp_x [get_attribute [get_timing_paths $my_path -pba_mode path] arrival]
	set tmp_y [get_attribute [get_attribute [get_timing_paths $my_path -pba_mode path] launch_clock_paths] arrival]
	echo [expr $tmp_x - $tmp_y] >> ${spice_folder}/slack_data_pt.txt
	# $tmp_res >> ${spice_folder}/slack_data_pt.txt
	# capture:
	get_attribute [get_attribute [get_timing_paths $my_path -pba_mode path] capture_clock_paths] arrival >> ${spice_folder}/slack_capture_pt.txt
	# common:
	# report_attribute [get_attribute [get_timing_paths $my_path -pba_mode path] capture_clock_paths]
	# fan_out:
	set tmp_list [split [get_attribute [get_nets -of_objects [get_attribute [get_attribute [get_timing_paths $my_path -pba_mode path] points] object]] number_of_leaf_loads] " "]
	set ttl 0
	foreach nxt $tmp_list {
		incr ttl $nxt
	}
	echo $ttl >> ${spice_folder}/ttl_fanout_pt.txt
# ############################################################################################################################################################	
}
exit	
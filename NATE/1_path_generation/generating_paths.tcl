# #######################################
# ####	revise these if needed:
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
# first group all paths from reg to reg:
group_path -name input_paths -from [get_ports * -filter "direction==in"]
group_path -name output_paths -to [get_ports * -filter "direction==out"]
set path_number $env(numofpaths)
set nworst_ $env(nworst_)
if {[file isdirectory ${workfolder}/Paths]} {
	file delete -force -- ${workfolder}/Paths
}
file mkdir ${workfolder}/Paths

if {[file isdirectory ${workfolder}/generated_inputs/num_of_paths]} {
	file delete -force -- ${workfolder}/generated_inputs/num_of_paths
}
file mkdir ${workfolder}/generated_inputs/num_of_paths
# #######################################
# procedure to generate paths
proc points_proc {workfolder path_number} {
	set path_counter 0
	foreach_in_collection pathss [get_timing_paths -pba_mode path -group clktop -path_type full_clock_expanded -nworst ${nworst_} -max_paths ${path_number} -slack_lesser_than 20] {
		echo "$path_counter"
		file mkdir ${workfolder}/Paths/Path${path_counter}				
		file mkdir ${workfolder}/Paths/Path${path_counter}/launch
		file mkdir ${workfolder}/Paths/Path${path_counter}/capture
		file mkdir ${workfolder}/Paths/Path${path_counter}/launch/generated_inputs
		file mkdir ${workfolder}/Paths/Path${path_counter}/capture/generated_inputs
		##########################################					bellow is for generating path in text files					##########################################
		##################################################################################################################################################################
		report_timing $pathss -pba_mode path -path_type full_clock_expanded >> ${workfolder}/Paths/Path${path_counter}/timing_report.txt
		set launch_timing_path [open "${workfolder}/Paths/Path${path_counter}/the_path_origin.txt" w]
		set capture_timing_path [open "${workfolder}/Paths/Path${path_counter}/the_path_origin_for_capture.txt" w]

		set list_rise_fall_capture []
		set list_rise_fall_launch []

		set start_point [get_attribute [get_attribute $pathss startpoint] full_name]
		# set start_point [get_attribute [get_attribute [get_attribute $pathss launch_clock_paths] startpoint] full_name]
		set end_point [get_attribute [get_attribute $pathss endpoint] full_name]
		set capture_end [get_attribute [get_attribute $pathss capture_clock_paths] endpoint]
		set start_point_rise_fall [lindex [get_attribute [get_attribute $pathss points] rise_fall] 0]
		set end_point_rise_fall [lindex [get_attribute [get_attribute $pathss points] rise_fall] end]
		if {$start_point_rise_fall == "rise"} {
			set sp_rf "-rise_from"
		} else {
			set sp_rf "-fall_from"
		}
		if {$end_point_rise_fall == "rise"} {
			set ep_rf "-rise_to"
		} else {		
			set ep_rf "-fall_to"
		}		

		# launch
		foreach_in_collection data_points [get_attribute $pathss points] {
			set check_rise_fall_data [get_attribute $data_points rise_fall]
			set check_direction_data [get_attribute [get_attribute $data_points object] direction]
			if {$check_rise_fall_data == "rise" && $check_direction_data == "out"} {
				lappend list_rise_fall_launch -rise_through
				lappend list_rise_fall_launch [get_attribute [get_attribute $data_points object] full_name]
			}
			if {$check_rise_fall_data == "fall" && $check_direction_data == "out"} {
				lappend list_rise_fall_launch -fall_through
				lappend list_rise_fall_launch [get_attribute [get_attribute $data_points object] full_name]
			}
		}				
		###############################################################################################################################################################			
		# capture		
		set capture_point [get_timing_paths -pba_mode path -path_type full_clock_expanded -from $capture_end -nworst 1 -max_paths 1 -slack_lesser_than 40]
		if {[llength $capture_point]==0} {
			set capture_point [get_timing_paths -pba_mode path -path_type full_clock_expanded -from [get_cells -of_objects $capture_end] -nworst 1 -max_paths 1 -slack_lesser_than 40]
		}
		set start_point_capture [get_attribute [get_attribute $capture_point startpoint] full_name]
		report_timing $capture_point -pba_mode path -path_type full_clock_expanded >> ${workfolder}/Paths/Path${path_counter}/timing_report_capture.txt
		#set start_point_capture [get_attribute [get_attribute [get_attribute $capture_point launch_clock_paths] startpoint] full_name]
		set end_point_capture [get_attribute [get_attribute $capture_point endpoint] full_name]
		set start_point_capture_rise_fall [lindex [get_attribute [get_attribute $capture_point points] rise_fall] 0]
		set end_point__capture_rise_fall [lindex [get_attribute [get_attribute $capture_point points] rise_fall] end]
		if {$start_point_capture_rise_fall == "rise"} {
			set sp_rf_c "-rise_from"
		} else {
			set sp_rf_c "-fall_from"
		}
		if {$start_point_capture_rise_fall == "rise"} {
			set ep_rf_c "-rise_to"
		} else {		
			set ep_rf_c "-fall_to"
		}		
		foreach_in_collection capture_points [get_attribute [get_attribute $capture_point launch_clock_paths] points] {
		
			set check_rise_fall_capture [get_attribute $capture_points rise_fall]
			set check_direction_capture [get_attribute [get_attribute $capture_points object] direction]
			if {$check_rise_fall_capture == "rise" && $check_direction_capture == "out"} {
				lappend list_rise_fall_capture -rise_through
				lappend list_rise_fall_capture [get_attribute [get_attribute $capture_points object] full_name]
			}
			if {$check_rise_fall_capture == "fall" && $check_direction_capture == "out"} {
				lappend list_rise_fall_capture -fall_through
				lappend list_rise_fall_capture [get_attribute [get_attribute $capture_points object] full_name]
			}
		}
		
		###############################################################################################################################################################	
		# launch out
		puts  -nonewline $launch_timing_path "set my_path "
		puts  -nonewline $launch_timing_path {[}
		# ask how to specify if it's rise or fall for start point? attribute was not found
		puts  -nonewline $launch_timing_path "get_timing_path -pba_mode path -path_type full_clock_expanded $sp_rf $start_point $ep_rf $end_point $list_rise_fall_launch"

		puts  -nonewline $launch_timing_path  {]}
		close $launch_timing_path		
		###############################################################################################################################################################	
		# capture out	
		puts  -nonewline $capture_timing_path "set my_path_capture "
		puts  -nonewline $capture_timing_path {[}
		
		puts  -nonewline $capture_timing_path "get_timing_path -pba_mode path -path_type full_clock_expanded $sp_rf_c $start_point_capture $ep_rf_c $end_point_capture"
		puts  -nonewline $capture_timing_path  {]}
		close $capture_timing_path
		incr path_counter
	}		
	
	puts "#=====================" 
	set tem_folder [open "${workfolder}/generated_inputs/num_of_paths/num_of_paths.txt" w]
	puts -nonewline $tem_folder "$path_counter"
	close $tem_folder
	return $path_counter
}
# #######################################
# #######################################
set path_counter [points_proc $workfolder $path_number]

exit


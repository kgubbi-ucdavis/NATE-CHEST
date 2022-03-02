# ###############################	Trojan Insertion Procedure 		#######################################
# this will insert trojan, route and save it in a new MW CEL.
# mw_CL_name			:	name of the MW CEL library for saving the new design containing HT
# targeted_path_index	:	index of targeted path for referencing
# payload_strength		:	should be one of these :<1 2>. strength of the payload gate
# trigger_net_list		:	should not be empty. nets targeted for trigger connection
# payload_cell_pin		:	output pin of the cell targeted for payload connection
# ##		NOTES		:	1- trigger cell strength is constant "x2"
# ##						2- all TP gate are "XOR" gates
# ######################
# ##						3- trigger cell strength is constant "x2"
# ##						2- all TT gate are "AND" gates
# procedure to insert trojans:
proc insert_trojan {mw_CL_name targeted_path_index payload_strength payload_cell_pin trigger_net_list HT_dataset_path} {
	set TT_x 2
	set nets_to_be_routed []
	set payload_cell [get_attribute [get_cells -of_objects $payload_cell_pin] name]
	set_object_fixed_edit [get_cells *] 1
	# ########################     find the point to connect the TP to:
	set our_net [get_nets -of_objects ${payload_cell_pin}]
	set list_of_nets []
	# ########################     inserting and connecting TP:
	create_cell trojan_TP_${payload_cell} XOR2X${payload_strength}_RVT
	create_net trj_TP_${payload_cell}_A1
	create_net trj_TP_${payload_cell}_A2
	connect_net trj_TP_${payload_cell}_A1 [get_pins trojan_TP_${payload_cell}/A1]
	connect_net trj_TP_${payload_cell}_A2 [get_pins trojan_TP_${payload_cell}/A2]
	disconnect_net $our_net [get_pins ${payload_cell_pin}]
	connect_net $our_net [get_pins trojan_TP_${payload_cell}/Y]
	connect_net trj_TP_${payload_cell}_A2 [get_pins ${payload_cell_pin}]
	lappend list_of_nets trj_TP_${payload_cell}_A1
	lappend nets_to_be_routed $our_net
	lappend nets_to_be_routed trj_TP_${payload_cell}_A1
	lappend nets_to_be_routed trj_TP_${payload_cell}_A2
	# ########################     create TT gates:
	# check if no trigger is needed:
	set num_of_triggers [llength ${trigger_net_list}]
	if {$num_of_triggers == 1} {
		disconnect_net trj_TP_${payload_cell}_A1 [get_pins trojan_TP_${payload_cell}/A1]
		remove_net trj_TP_${payload_cell}_A1
		connect_net [lindex $trigger_net_list 0] [get_pins trojan_TP_${payload_cell}/A1]
	} else {
	# if trigger is needed
		for {set x 1} {$x<$num_of_triggers} {incr x} {
			create_cell trojan_TT_${x} AND2X${TT_x}_RVT
			create_net trj_TT_${x}_A1
			create_net trj_TT_${x}_A2
			connect_net trj_TT_${x}_A1 [get_pins trojan_TT_${x}/A1]
			connect_net trj_TT_${x}_A2 [get_pins trojan_TT_${x}/A2]
			lappend nets_to_be_routed trj_TT_${x}_A1
			lappend nets_to_be_routed trj_TT_${x}_A2			
		}
		# ########################     connect TT gates together:
		set list_of_TT_inputs []
		for {set i 1} {$i<$num_of_triggers} {incr i} {
			connect_net [lindex $list_of_nets [expr $i-1]] [get_pins trojan_TT_${i}/Y]
			lappend list_of_nets trj_TT_${i}_A1
			lappend list_of_nets trj_TT_${i}_A2
			lappend list_of_TT_inputs trj_TT_${i}_A1
			lappend list_of_TT_inputs trj_TT_${i}_A2
			set idx [lsearch $list_of_TT_inputs [lindex $list_of_nets [expr $i - 1]]]
			set list_of_TT_inputs [lreplace $list_of_TT_inputs $idx $idx]
		}
		# ########################     connect TT gates to targeted nets:
		for {set i 0} {$i<$num_of_triggers} {incr i} {
			set pin_of_trigger_gate [get_pins -of_objects [lindex $list_of_TT_inputs $i]]
			disconnect_net [lindex $list_of_TT_inputs $i] [get_pins -of_objects [lindex $list_of_TT_inputs $i]]
			remove_net [lindex $list_of_TT_inputs $i]
			set idx [lsearch $nets_to_be_routed [lindex $list_of_TT_inputs $i]]
			set nets_to_be_routed [lreplace $nets_to_be_routed $idx $idx]
			connect_net [lindex $trigger_net_list $i] $pin_of_trigger_gate
		}
	}
	# ########################     place, route and save the new MW CEL:
	place_eco_cells -unplaced_cells
	route_zrt_group -nets [get_nets $nets_to_be_routed]
	set_object_fixed_edit [get_cells *] 0
	# write_verilog ${HT_dataset_path}/netlist_trojans/${mw_CL_name}_trojan_${targeted_path_index}.v
	report_timing
	write_parasitics -output ${HT_dataset_path}/netlist_trojans/${mw_CL_name}_trojan_${targeted_path_index}
	save_mw_cel -as ${mw_CL_name}_trojan_${targeted_path_index}
	close_mw_cel
	open_mw_cel $mw_CL_name
}
# #########################################################################################################

# ###############################	  Find target for TP gate 		#######################################
# this will find the output pin of a cell which trojan payload is connected to. (payload_cell_pin)
# path_file_location	:	/scratch/kgubbi/Paths_of_designs/s38417/T1p4/Paths
# targeted_path_index	:	index of targeted path for referencing
# procedure to find the location from specified path:
proc payload_pin {path_file_location targeted_path_index} {
	set fp [open "${path_file_location}/Path${targeted_path_index}/launch/generated_inputs/delay_info_min.txt" r]
	set file_data [read $fp]
	close $fp
	set data1 [split $file_data "\n"]
	set data_elem [split [lindex $data1 4] " "]
	# if only register
	set temp_length [expr [llength $data_elem]/2 -1]
	if {[regexp {/Y} [lindex $data_elem $temp_length]]} {
		set gigili [lindex $data_elem $temp_length]
		set fault_pin [lindex $data_elem [expr $temp_length +1]]
		set third_LVT [lindex $data_elem [expr $temp_length +3]]
	} else {
		set gigili [lindex $data_elem [expr $temp_length +1]]
		set fault_pin [lindex $data_elem [expr $temp_length +2]]
		set third_LVT [lindex $data_elem [expr $temp_length +4]]
	}
	return [list $gigili $fault_pin $third_LVT]
}
# #########################################################################################################

# ###############################	  Find target for TT gates 		#######################################
# this will find the nets which trojan trigger is connected to. (trigger_net_list)
# path_file_location	:	/scratch/kgubbi/Paths_of_designs/s38417/T1p4/Paths
# targeted_path_index	:	index of targeted path for referencing
# number_of_TT_inputs	:	number of nets which TT gets connected to.
# payload_cell_pin		:	output pin of the cell targeted for payload connection
# lower_radius			:	lower radius for distance of TT inputs
# upper_radius			:	upper radius for distance of TT inputs
# procedure to find the location from specified path:
proc trigger_nets {path_file_location targeted_path_index number_of_TT_inputs payload_cell_pin lower_radius upper_radius min max} {
	set TP_cel [get_cells -of_objects $payload_cell_pin]
	set TP_coordinates [lindex [get_attribute $TP_cel bbox] 0]
	# choose random from 20 to 1500 except targeted_path_index:
	# set min 5
	# set max 99
	set trigger_net_list []
	set trigger_path_list []
	set condition_inputs 0
	while {$condition_inputs < $number_of_TT_inputs} {
		set condition_except_TP_path 0
		while {$condition_except_TP_path < 1} {
			set rndm_path [expr {int(rand() * ($max + 1 - $min)) + $min}]
			# check if its same as payload path:
			if {[lsearch -exact $targeted_path_index $rndm_path] < 0} {
				# check if its not already taken:
				if {[lsearch -exact $trigger_path_list $rndm_path] < 0} {
					set condition_except_TP_path 1
				}
			}
		}
		set fp [open "${path_file_location}/Path${rndm_path}/launch/generated_inputs/delay_info_min.txt" r]
		set file_data [read $fp]
		close $fp
		set data1 [split $file_data "\n"]
		set data_elem [split [lindex $data1 4] " "]
		# we dont want a path with only one register:
		if {[llength $data_elem] > 3} {
			set temp_length [expr [llength $data_elem] -1]
			set targt_cel [get_cells -of_objects [lindex $data_elem $temp_length]]
			# check if it has both raise and fall options:
			set trigger_option_rise [llength [get_timing_paths -rise_through [get_attribute [lindex $data_elem $temp_length] full_name]]]
			set trigger_option_fall [llength [get_timing_paths -fall_through [get_attribute [lindex $data_elem $temp_length] full_name]]]
			if {$trigger_option_rise > 0 && $trigger_option_fall > 0} {
				# we check the distance of net from TP:
				set TT_coord [lindex [get_attribute $targt_cel bbox] 0]
				set distance_x [expr [lindex $TT_coord 0] - [lindex $TP_coordinates 0]]
				set distance_y [expr [lindex $TT_coord 1] - [lindex $TP_coordinates 1]]
				set distance_x2 [expr $distance_x*$distance_x]
				set distance_y2 [expr $distance_y*$distance_y]
				set distance [expr sqrt([expr $distance_x2 + $distance_y2])]
				if {$distance > $lower_radius && $distance < $upper_radius} {
					lappend trigger_path_list $rndm_path
					lappend trigger_net_list [get_attribute [get_nets -of_objects [lindex $data_elem $temp_length]] name]
					set condition_inputs [expr $condition_inputs + 1]
				}			
			}
		}	
	}
	return [list $trigger_net_list $trigger_path_list]
}
# #########################################################################################################

# ###############################	  Find target for TP paths 		#######################################
# this will find the paths which trojan payload is inserted into. (targeted_path_index)
# path_file_location	:	/scratch/kgubbi/Paths_of_designs/s38417/T1p4/Paths
# from_path				:	lower limit path number
# to_path				:	upper limit path number
# excluded_paths		:	paths that are already selected before for insertion or FP
# num_of_paths			:	number of desired paths
# procedure to find the path index and payload gate:
proc payload_path_index {path_file_location from_path to_path num_of_paths excluded_paths} {
	set min $from_path
	set max $to_path
	set payload_path_list []
	set counter_paths 0
	while {$counter_paths < $num_of_paths} {
		set rndm_path [expr {int(rand() * ($max + 1 - $min)) + $min}]
		if {[lsearch $excluded_paths $rndm_path] == -1 && [lsearch $payload_path_list $rndm_path] == -1} {
			set fp [open "${path_file_location}/Path${rndm_path}/launch/generated_inputs/delay_info_min.txt" r]
			set file_data [read $fp]
			close $fp
			set data1 [split $file_data "\n"]
			set data_elem [split [lindex $data1 4] " "]
			# we dont want a path with only one register:
			if {[llength $data_elem] > 7} {
				set temp_length [expr [llength $data_elem]/2 -1]
				if {[regexp {/Y} [lindex $data_elem $temp_length]]} {
					set gigili [get_attribute [get_cells -of_objects [lindex $data_elem $temp_length]] ref_name]
				} else {
					set gigili [get_attribute [get_cells -of_objects [lindex $data_elem [expr $temp_length +1]]] ref_name]
				}
				set counter_paths [expr $counter_paths + 1]
				lappend payload_path_list $rndm_path	
			}
		}	
	}
	return $payload_path_list
}
# #########################################################################################################

# ########################		Check if path exist after insertion 		###############################
# this will check if a path exit after trojan insertion. it's similar to insertion procedure, without saving the design.
# mw_CL_name			:	name of the MW CEL library for saving the new design containing HT
# targeted_path_index	:	index of targeted path for referencing
# payload_strength		:	should be one of these :<1 2>. strength of the payload gate
# trigger_net_list		:	should not be empty. nets targeted for trigger connection
# payload_cell_pin		:	output pin of the cell targeted for payload connection
# ##		NOTES		:	1- trigger cell strength is constant "x2"
# ##						2- all TP gate are "XOR" gates
# ######################
# ##						3- trigger cell strength is constant "x2"
# ##						2- all TT gate are "AND" gates
# procedure to check insertion:
proc check_insert_trojan {path_file_location mw_CL_name targeted_path_index payload_strength payload_cell_pin trigger_net_list} {
	set TT_x 2
	set nets_to_be_routed []
	set payload_cell [get_attribute [get_cells -of_objects $payload_cell_pin] name]
	set_object_fixed_edit [get_cells *] 1
	# ########################     find the point to connect the TP to:
	set our_net [get_nets -of_objects ${payload_cell_pin}]
	set list_of_nets []
	# ########################     inserting and connecting TP:
	create_cell trojan_TP_${payload_cell} XOR2X${payload_strength}_RVT
	create_net trj_TP_${payload_cell}_A1
	create_net trj_TP_${payload_cell}_A2
	connect_net trj_TP_${payload_cell}_A1 [get_pins trojan_TP_${payload_cell}/A1]
	connect_net trj_TP_${payload_cell}_A2 [get_pins trojan_TP_${payload_cell}/A2]
	disconnect_net $our_net [get_pins ${payload_cell_pin}]
	connect_net $our_net [get_pins trojan_TP_${payload_cell}/Y]
	connect_net trj_TP_${payload_cell}_A2 [get_pins ${payload_cell_pin}]
	lappend list_of_nets trj_TP_${payload_cell}_A1
	lappend nets_to_be_routed $our_net
	lappend nets_to_be_routed trj_TP_${payload_cell}_A1
	lappend nets_to_be_routed trj_TP_${payload_cell}_A2
	# ########################     create TT gates:
	# check if no trigger is needed:
	set num_of_triggers [llength ${trigger_net_list}]
	if {$num_of_triggers == 1} {
		disconnect_net trj_TP_${payload_cell}_A1 [get_pins trojan_TP_${payload_cell}/A1]
		remove_net trj_TP_${payload_cell}_A1
		connect_net [lindex $trigger_net_list 0] [get_pins trojan_TP_${payload_cell}/A1]
	} else {
	# if trigger is needed
		for {set x 1} {$x<$num_of_triggers} {incr x} {
			create_cell trojan_TT_${x} AND2X${TT_x}_RVT
			create_net trj_TT_${x}_A1
			create_net trj_TT_${x}_A2
			connect_net trj_TT_${x}_A1 [get_pins trojan_TT_${x}/A1]
			connect_net trj_TT_${x}_A2 [get_pins trojan_TT_${x}/A2]
			lappend nets_to_be_routed trj_TT_${x}_A1
			lappend nets_to_be_routed trj_TT_${x}_A2			
		}
		# ########################     connect TT gates together:
		set list_of_TT_inputs []
		for {set i 1} {$i<$num_of_triggers} {incr i} {
			connect_net [lindex $list_of_nets [expr $i-1]] [get_pins trojan_TT_${i}/Y]
			lappend list_of_nets trj_TT_${i}_A1
			lappend list_of_nets trj_TT_${i}_A2
			lappend list_of_TT_inputs trj_TT_${i}_A1
			lappend list_of_TT_inputs trj_TT_${i}_A2
			set idx [lsearch $list_of_TT_inputs [lindex $list_of_nets [expr $i - 1]]]
			set list_of_TT_inputs [lreplace $list_of_TT_inputs $idx $idx]
		}
		# ########################     connect TT gates to targeted nets:
		for {set i 0} {$i<$num_of_triggers} {incr i} {
			set pin_of_trigger_gate [get_pins -of_objects [lindex $list_of_TT_inputs $i]]
			disconnect_net [lindex $list_of_TT_inputs $i] [get_pins -of_objects [lindex $list_of_TT_inputs $i]]
			remove_net [lindex $list_of_TT_inputs $i]
			set idx [lsearch $nets_to_be_routed [lindex $list_of_TT_inputs $i]]
			set nets_to_be_routed [lreplace $nets_to_be_routed $idx $idx]
			connect_net [lindex $trigger_net_list $i] $pin_of_trigger_gate
		}
	}
	# ########################     place, route and save the new MW CEL:
	place_eco_cells -unplaced_cells
	route_zrt_group -nets [get_nets $nets_to_be_routed]
	set_object_fixed_edit [get_cells *] 0
	# launch and data path:
	set fp [open "${path_file_location}/Path${targeted_path_index}/the_path_origin.txt" r]
	set file_data [read $fp]
	close $fp
	set data1 [split $file_data "\n"]
	set data_elem [lindex $data1 0]
	set data_elem [string map {{set my_path [get_timing_path -pba_mode path -path_type full_clock_expanded} "get_timing_paths" {]} ""} $data_elem]
	set out_checker_launch [llength [eval $data_elem]]
	# capture path:
	set fp [open "${path_file_location}/Path${targeted_path_index}/the_path_origin_for_capture.txt" r]
	set file_data [read $fp]
	close $fp
	set data1 [split $file_data "\n"]
	set data_elem [lindex $data1 0]
	set data_elem [string map {{set my_path_capture [get_timing_path -pba_mode path -path_type full_clock_expanded} "get_timing_paths" {]} ""} $data_elem]
	set out_checker_capture [llength [eval $data_elem]]
	# both conditions
	set out_checker [expr $out_checker_launch*$out_checker_capture]
	close_mw_cel
	open_mw_cel $mw_CL_name
	return $out_checker
}
# #########################################################################################################


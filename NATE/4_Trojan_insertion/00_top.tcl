source ./config.tcl
# paths used to insert trojan before, or used for false positive:
if { [file exist "${HT_dataset_path}/HT_exclude_database.txt"] == 1} {
	echo "yess"
	set file_exclude_apths [open "${HT_dataset_path}/HT_exclude_database.txt" r]
	set excluded_paths_line [read $file_exclude_apths]
	close $file_exclude_apths
	set excluded_paths [regexp -inline -all -- {\S+} $excluded_paths_line]
} else {
	set excluded_paths {}
}
echo $excluded_paths
# ###############################################################
# ###############################################################
if {[file isdirectory ${HT_dataset_path}/netlist_trojans]} {
	# file delete -force -- ${HT_dataset_path}/netlist_trojans
	echo "folder exist"
} else {
	file mkdir ${HT_dataset_path}/netlist_trojans
}

source ./HT_insertion_proces.tcl
set trojan_path_database [open "${HT_dataset_path}/HT_location_database.txt" a]
puts -nonewline $trojan_path_database "trojan_design_name payload_strength number_of_TT_inputs lower_radius upper_radius targeted_path_index payload_cell_pin " 
for {set xx 0} {$xx < $number_of_TT_inputs} {incr xx} {
	puts -nonewline $trojan_path_database "trigger_net_${xx} " 
}
for {set xx 0} {$xx < $number_of_TT_inputs} {incr xx} {
	puts -nonewline $trojan_path_database "trigger_path_${xx} " 
}
puts -nonewline $trojan_path_database "payload_pin_stuck_at_fault" 
puts $trojan_path_database ""

set num_TP $num_payloads
while {$num_TP > 0} {
	# first, find payload paths:
	set payload_paths [payload_path_index $path_file_location $from_path $to_path $num_TP $excluded_paths]
	set excluded_paths [concat $excluded_paths $payload_paths]
	foreach targeted_path_index $payload_paths {
		# find the cell that TP is connected to:
		set payload_cell_pin_and_fault [payload_pin $path_file_location $targeted_path_index]
		set payload_cell_pin [lindex $payload_cell_pin_and_fault 0]
		set payload_pin_fault [lindex $payload_cell_pin_and_fault 1]
		set third_LVT_pin [lindex $payload_cell_pin_and_fault 2]
		# find TT nets, but notice that we should make sure that the combination of TP and TTs still produce the previous path_report:
		set check_combination 0
		set couter_to_change_TP 0
		while {$check_combination == 0 && $couter_to_change_TP < 3} {
			set trigger_net_list_path [trigger_nets $path_file_location $excluded_paths $number_of_TT_inputs $payload_cell_pin $lower_radius $upper_radius $from_path $to_path]
			set trigger_net_list [lindex $trigger_net_list_path 0]
			set trigger_path_list [lindex $trigger_net_list_path 1]
			set checker_variable 0
			set checker_variable [check_insert_trojan $path_file_location $mw_CL_name $targeted_path_index $payload_strength $payload_cell_pin $trigger_net_list]
			set couter_to_change_TP [expr $couter_to_change_TP + 1]
			if {$checker_variable > 0} {
				set check_combination 1
			}
		}
		if {$check_combination == 1} {
			insert_trojan $mw_CL_name $targeted_path_index $payload_strength $payload_cell_pin $trigger_net_list $HT_dataset_path
			puts $trojan_path_database "${mw_CL_name}_trojan_${targeted_path_index} ${payload_strength} ${number_of_TT_inputs} ${lower_radius} ${upper_radius} ${targeted_path_index} ${payload_cell_pin} ${trigger_net_list} ${trigger_path_list} ${payload_pin_fault}" 	
			set num_TP [expr $num_TP - 1]
			set excluded_paths [concat $excluded_paths $trigger_path_list]
		}
	}
}


close $trojan_path_database
# write out the exclude list
set exclude_path_database [open "${HT_dataset_path}/HT_exclude_database.txt" w]
foreach ex_path $excluded_paths {
	puts -nonewline $exclude_path_database "$ex_path "
}
close $exclude_path_database

exit







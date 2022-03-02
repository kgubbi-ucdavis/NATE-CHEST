# #######################################
# ####	revise these:
source ./config.tcl
set workfolder "../../Designs/${Design_name}/${Design_tag_name}"
set spice_folder "${workfolder}/NN_training_ICC"
cd "${milkyway_lib_dir}"
cd ../
set clock_ports ${clock_ports_name}

if {[file isdirectory ${spice_folder}]} {
	file delete -force -- ${spice_folder}
}
file mkdir ${spice_folder}
# #######################################
set fp [open "${workfolder}/generated_inputs/num_of_paths/num_of_paths.txt" r]
set number_of_files [read $fp]
close $fp

for {set i 0} {$i<$number_of_files} {incr i} {
	echo $i
# ############################################################################################################################################################
# for net info >>> :
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
		if {[lindex $cap_cels ${y}] != $clock_ports} {
			lappend capture_cel_list [get_attribute [get_nets -of_objects [lindex $cap_cels ${y}]] full_name]
		}
	}
	set cap_cel_list [lsort -unique $capture_cel_list]
	# launch + common:
	for {set y 0} {$y<$lan_num_of_cels} {incr y} {
		if {[lindex $lan_cels ${y}] != $clock_ports} {
			lappend launch_cel_list [get_attribute [get_nets -of_objects [lindex $lan_cels ${y}]] full_name]
		}
	}
	set lan_cel_list [lsort -unique $launch_cel_list]
	# data:
	for {set y 2} {$y<$dat_num_of_cels} {incr y} {
		if {[lindex $dat_cels ${y}] != $clock_ports} {
			lappend data_cel_list [get_attribute [get_nets -of_objects [lindex $dat_cels ${y}]] full_name]
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
	set m1 0
	set m2 0
	set m3 0
	set m4 0
	set m5 0
	set net_list []
	for {set y 0} {$y<[llength $cap_cel_list]} {incr y} {
		set net_list [regsub -all {\{|\}} [get_attribute [get_nets [lindex $cap_cel_list ${y}]] route_length] ""]
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M1"} {
				set m1 [expr $m1 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M2"} {
				set m2 [expr $m2 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M3"} {
				set m3 [expr $m3 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M4"} {
				set m4 [expr $m4 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M5"} {
				set m5 [expr $m5 + [lindex $net_list [expr $j + 1]] ]
			}
		}		
	}
	echo $m1 >> ${spice_folder}/net_m1_capture_pt.txt
	echo $m2 >> ${spice_folder}/net_m2_capture_pt.txt
	echo $m3 >> ${spice_folder}/net_m3_capture_pt.txt
	echo $m4 >> ${spice_folder}/net_m4_capture_pt.txt
	echo $m5 >> ${spice_folder}/net_m5_capture_pt.txt


	# now strength of launch:
	set m1 0
	set m2 0
	set m3 0
	set m4 0
	set m5 0
	set net_list []
	for {set y 0} {$y<[llength $lan_cel_list]} {incr y} {
		set net_list [regsub -all {\{|\}} [get_attribute [get_nets [lindex $lan_cel_list ${y}]] route_length] ""]
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M1"} {
				set m1 [expr $m1 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M2"} {
				set m2 [expr $m2 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M3"} {
				set m3 [expr $m3 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M4"} {
				set m4 [expr $m4 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M5"} {
				set m5 [expr $m5 + [lindex $net_list [expr $j + 1]] ]
			}
		}		
	}
	echo $m1 >> ${spice_folder}/net_m1_launch_pt.txt
	echo $m2 >> ${spice_folder}/net_m2_launch_pt.txt
	echo $m3 >> ${spice_folder}/net_m3_launch_pt.txt
	echo $m4 >> ${spice_folder}/net_m4_launch_pt.txt
	echo $m5 >> ${spice_folder}/net_m5_launch_pt.txt


	# now strength of data:
	set m1 0
	set m2 0
	set m3 0
	set m4 0
	set m5 0
	set net_list []
	for {set y 0} {$y<[llength $dat_cel_list]} {incr y} {
		set net_list [regsub -all {\{|\}} [get_attribute [get_nets [lindex $dat_cel_list ${y}]] route_length] ""]
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M1"} {
				set m1 [expr $m1 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M2"} {
				set m2 [expr $m2 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M3"} {
				set m3 [expr $m3 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M4"} {
				set m4 [expr $m4 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M5"} {
				set m5 [expr $m5 + [lindex $net_list [expr $j + 1]] ]
			}
		}		
	}
	echo $m1 >> ${spice_folder}/net_m1_data_pt.txt
	echo $m2 >> ${spice_folder}/net_m2_data_pt.txt
	echo $m3 >> ${spice_folder}/net_m3_data_pt.txt
	echo $m4 >> ${spice_folder}/net_m4_data_pt.txt
	echo $m5 >> ${spice_folder}/net_m5_data_pt.txt



	# now strength of common:
	set m1 0
	set m2 0
	set m3 0
	set m4 0
	set m5 0
	set net_list []
	for {set y 0} {$y<[llength $com_cel_list]} {incr y} {
		set net_list [regsub -all {\{|\}} [get_attribute [get_nets [lindex $com_cel_list ${y}]] route_length] ""]
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M1"} {
				set m1 [expr $m1 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M2"} {
				set m2 [expr $m2 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M3"} {
				set m3 [expr $m3 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M4"} {
				set m4 [expr $m4 + [lindex $net_list [expr $j + 1]] ]
			}
		}
		for {set j 0} {$j<[llength $net_list]} {incr j} {
			if {[lindex $net_list ${j}] == "M5"} {
				set m5 [expr $m5 + [lindex $net_list [expr $j + 1]] ]
			}
		}		
	}
	echo $m1 >> ${spice_folder}/net_m1_common_pt.txt
	echo $m2 >> ${spice_folder}/net_m2_common_pt.txt
	echo $m3 >> ${spice_folder}/net_m3_common_pt.txt
	echo $m4 >> ${spice_folder}/net_m4_common_pt.txt
	echo $m5 >> ${spice_folder}/net_m5_common_pt.txt
# <<< for net info
# ############################################################################################################################################################	
}
exit	
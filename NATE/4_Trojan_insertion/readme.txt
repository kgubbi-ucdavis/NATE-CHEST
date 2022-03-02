you need to run feature extraction script in advance to generate a set of timing-paths
this script inserts a a number of Trojan Circuits into clean design
edit the config.tcl file based on desired Trojan Circuit
steps:
1- change directory to 4_Trojan_insertion
2- load routed design with necessary libraries
3- revise the config.txt
* keep the number of TT 4. otherwise you need to revise the "find_malic_paths.py" script in "5_SPICE_Trojan" folder.
* the current script consider 4 TT nets. Note that in practice we do not have information about the Trojan Circuit.
* this is only to generate a dataset that contains the slacks of trojan paths, so keep tracking of trojans is important
* note that the detection algorithm does not consider the structure of Trojan Circuit and has no information about trojans.
4- run the top.tcl
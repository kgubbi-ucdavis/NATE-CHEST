#we use a make file to PnR, the make file assigns a design name and tag name. here we set them in case there are other PnR flows:
set dsgn_name $design			# name of the design folder
set tag_name ${tag}				# tag name
set mw_CL_name ${DESIGN_NAME}	# name of the top module
set path_file_location "../../Designs/${dsgn_name}/${tag_name}/Paths"		# directorie in which path folder is located. feature extraction needs to be run in advance
set HT_dataset_path "../../Designs/${dsgn_name}/${tag_name}"				# the folder contains the results
set payload_strength 1			# set desired payload strength of Trojan Payload gate

set number_of_TT_inputs 4		# set number of inputs of Trigger circuit
# this script randomely select a cell as victim cell to insert Payload
# to select the victim Triggering nets, we specify two radius in which limits the location of victim net
set lower_radius 90
set upper_radius 150
# in feature extraction script, we extract a set of timing paths. for simplicity we use the same list of timing-paths to insert Trojans
# we need to assign a range within the timing paths, so this script choose a path randomely, and insert the Payload in that path 
set from_path 20
set to_path 28000
# #####################
set num_payloads 15				# assign desired number of Trojan Circuits
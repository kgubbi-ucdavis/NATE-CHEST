For NATE, the concept is to build the dataset, train the model, and run detection.
The assumption is that we already have a trusted GDSII, and the Clock Frequency Sweeping test results of a suspicious fabrticated chip.
the "Trojan insertion" and "SPICE" simulation target to generate slacks of the malicious fabricated chip (in case there is no suspicious IC)
If you have the GDSII of a clean design, plus the timing information of malicious fabricated chip of that exact GDSII, then skip "trojan insertion" and "SPICE" simulations

steps:

Pre-NATE:
	you should have followings before running the NATE:
	1- PnR a benchmark > GDSII
	

For NATE:
* note for each step there are readme file and config file in each directory *
	1- generate a list of timing paths with "1_path_generation"
	2- extract features with "2_feature_extraction"
	* in case you do not have a suspicious fabricated chip: *
		* 3- run SPICE simulation for trusted design, via "3_SPICE_clean". Later on we replace the SPICE result of malicious paths with those of this simulation
		*	the reason is to limit the number of trojan-infected paths and increase the coverness of Trojans, and have a more reliable validation
		* 4- insert Trojan with "4_Trojan_insertion"
		* steps 3 and 4 can get done in parallel
		* 5- run SPICE simulation for Trojan paths with "5_SPICE_Trojan"
	6- collect labels and create the dataset with "6_generate_dataset"
	7- train the NN model with "7_train_NN", the script is for both MLP, and Stacked models.
	8- run Detection with "8_detection" folder
	* detection scripts also generates diagnostic information to find victimized nets




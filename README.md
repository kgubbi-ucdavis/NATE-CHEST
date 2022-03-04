# UC Davis NATE (CHEST)
UC Davis NATE - A Neural Network Assisted Timing Profiler for Hardware Trojan Detection

> UC Davis NATE is a methodology for Hardware Trojan detection. UC Davis NATE does not require a Golden IC. Instead, it trains a Neural Network to act as a process tracking watchdog for correlating the static timing data (produced at design time) to the delay information obtained from clock frequency sweeping (at test time) for the purpose of Trojan detection. Using the UC Davis NATE flow, close to 90% of Hardware Trojans in the simulated scenarios are detected.

Short Video Demo: https://youtu.be/twKXFVFdROE

Dependancies:
```
Synopsys IC Compiler 2
Synopsys Primetime 
Python3 
```

Python Module dependancies:
```
Keras                   2.3.1
Keras-Applications      1.0.8
Keras-Preprocessing     1.1.2
matplotlib              3.1.2
numpy                   1.17.4
pandas                  0.25.3
scikit-image            0.16.2
scikit-learn            0.22.2.post1
scipy                   1.3.3
sklearn                 0.0
tk                      0.1.0
```
<!-- 
## Table of Contents (Optional)

> If your `README` has a lot of info, section headers might be nice.

- [Installation](#installation)
- [Support](#support)
 -->

## UC Davis NATE

The concept is to build the dataset, train the model, and run detection.
The assumption is that we already have a trusted GDSII, and the Clock Frequency Sweeping test results of a suspicious fabrticated chip.
The "Trojan insertion" and "SPICE" simulation target to generate slacks of the malicious fabricated chip (in case there is no suspicious IC)
If you have the GDSII of a clean design, plus the timing information of malicious fabricated chip of that exact GDSII, then skip "trojan insertion" and "SPICE" simulations.

Steps:

Pre-NATE:
	you should have followings before running NATE:
	1- PnR a benchmark > GDSII

For UC Davis NATE:
* Note for each step there are readme file and config file (which needs to be edited) in each directory *
	1- Generate a list of timing paths with "1_path_generation"
	2- Extract features with "2_feature_extraction"
	* In case you do not have a suspicious fabricated chip: *
		* 3- Run SPICE simulation for trusted design, via "3_SPICE_clean". Later on, we replace the SPICE result of malicious paths with those of this simulation.
		*	The reason is to limit the number of trojan-infected paths and increase the coverness of Trojans, and have a more reliable validation
		* 4- insert Trojan with "4_Trojan_insertion"
		* steps 3 and 4 can get done in parallel
		* 5- Run SPICE simulation for Trojan paths with "5_SPICE_Trojan"
	6- Collect labels and create the dataset with "6_generate_dataset"
	7- Train the NN model with "7_train_NN", the script is for both MLP, and Stacked models.
	8- Run Detection with "8_detection" folder
	* Detection scripts also generates diagnostic information to find victimized nets


---

## Installation

### Clone

- Clone this repo to your local machine using 
```
git clone <use repo link from github>
```

### Running UC Davis NATE

Make sure to edit the config files before running these scripts.

```
$[user] cd NATE/1_path_generation
$[user] python3 top.py 
 
```
Run all required steps by moving into the appropriate directory and running the top script [Read the local readme files for more details]

Finally, run the detection sctipt (after training) to detect Hardware Trojans in a circuit.
```
.
.
.
$[user] cd ../NATE/8_detection
$[user] python3 top.py 

```

## Support

Reach out to me at one of the following places!

- Email at <a href="kgubbi@ucdavis.edu" target="_blank">`kgubbi@ucdavis.edu`</a>

---

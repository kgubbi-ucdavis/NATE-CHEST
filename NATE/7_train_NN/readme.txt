change directory to here
Edit config file: set the path for root directory root_path, and set the name of input file in_file and a file name for storing statistics of the used model res_file.

Note: some Trojan paths are randomly selected to get inserted in the train-set. This is for evaluating the impact of existence of Trojan in training the NN
this script is written to evaluate the existence of Trojan in 6 scenario, each contains 0, 10, 20, 30, 40, 50 Trojan paths in training-set.
you should randomly select these paths, and edit the "status" column of the dataset accordingly: change 'train_HT' to 'train_HT_10', 'train_HT_20', etc...
If you do not need this sweeping, change the script according to your requirements.

Also, the output file contains prediction for both "MLP" model and the "Stacking" model

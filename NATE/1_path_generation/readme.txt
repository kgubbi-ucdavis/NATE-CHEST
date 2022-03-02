for this part, we need to have the voltages from IR-ATA, as we also model the voltage variation
So first, find the final max and min voltages from IR-ATA project, then specify them in the config file. To start with, IR-ATA voltage has already been added to the config file.
then:
1- edit the config.txt
2- run top.py

* in case there is no fabricated chip, this code also generates SPICE netlist for each timing paths *
* for simplicity, we consider IR-ATA voltages to generate SPICE netlist out of PrimeTime. Otherwise, to have the SPICE simulations based on the cell voltages, collect the cell voltages from dynamic vectorless simulation and apply them in SPICE. *

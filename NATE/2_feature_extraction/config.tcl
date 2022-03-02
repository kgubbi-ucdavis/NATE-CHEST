set period_ "1.3"						# period of the design
set clock_ports_name "clk"				# name or list of the clock
# ########################################################################################
# our Physical Design uses a make file which generates a folder and a tag name per design:
set Design_name "AES128"				# name of the design
set Design_tag_name "b4"				# tag name of the design
set top_name_ "Top_PipelinedCipher"	# name of the top module in the gated netlist
# ########################################################################################
# directory of the constraint file:
set constraint_dir "/scratch/kgubbi/Golden_Folder/Designs/AES128/b4/2_Synthesis/results/Top_PipelinedCipher.mapped.sdc"
# ###########################
# Routed design is saved in milkyway format. the directory of the milkyway directory of the design:
set milkyway_lib_dir "/scratch/kgubbi/Golden_Folder/Designs/AES128/b4/7_Route/Top_PipelinedCipher_LIB_Route/"
# ###########################
# directory of parasitics file:
set para_dir_ "/scratch/kgubbi/Golden_Folder/Designs/AES128/b4/7_Route/results/parasitics.max"
# ########################################################################################
# library information:
# target library:
set target_lib_ "/cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_rvt/db_ccs/saed32rvt_tt1p05v125c.db"
# ###########################
# scaling library groups for different voltage corners:
set scaling_lib_1 "/cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_rvt/db_ccs/saed32rvt_tt0p78v125c.db"
set scaling_lib_2 "/cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_rvt/db_ccs/saed32rvt_tt0p85v125c.db"
set scaling_lib_3 "/cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_rvt/db_ccs/saed32rvt_tt1p05v125c.db"
# ###########################
# search path for Synopsys tool:
set search_path_ "/cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_lvt/db_ccs /cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_rvt/db_ccs /cm/shared/apps/synopsys/saed/SAED_EDK_32/lib/stdcell_hvt/db_ccs"

# set IR-ATA voltages:
set minvolt_ 0.95
set maxvolt_ 0.93

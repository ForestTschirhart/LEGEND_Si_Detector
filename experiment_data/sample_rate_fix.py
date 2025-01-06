import h5py
import numpy as np

### CONVERTS TIME BASE OF H5 FILE TO WHATEVER YOU WANT ###
### Different DAQs have different time bases, so this script can be used to convert the time base of an H5 file to match the actual time base
### If the default time base is used it may break depending on the DAQ in question


sample_period = 2.
sample_period_2 = 4.

# air runs
file_air1 = "DataR_CH1@DT5725_1146_air_run_1.lh5"
file_air2 = "DataR_CH1@DT5725_1146_air_run_3.lh5"
file_linamp = "DataR_CH1@DT5725_1146_lin_amp_0.lh5"

# random signals
crap_signals = "DataR_CH1@DT5730_1463_500um_random_signals.lh5"

# room tests
file_room1 = "DataR_CH1@DT5730_1463_150um_roomtest_analoghv.lh5"
file_room2 = "DataR_CH1@DT5730_1463_150um_roomtest_analoghv_break.lh5"
file_room3 = "DataR_CH1@DT5730_1463_150um_roomtest_dighv.lh5"
file_room4 = "DataR_CH1@DT5730_1463_150um_roomtest_alphas.lh5"


# Kammel Tests
k_file1 = "experiment_data/kammel_tests/raw/DataR_CH1@DT5730_1463_alpha_split.lh5" # path to raw file
k_file2 = "experiment_data/kammel_tests/raw/DataR_CH1@DT5730_1463_pulse_split.lh5"
k_file3 = "experiment_data/kammel_tests/raw/DataR_CH1@DT5730_1463_hole_backside.lh5"
k_file4 = "experiment_data/kammel_tests/raw/DataR_CH1@DT5730_1463_hole_frontside.lh5"
k_file5 = "experiment_data/kammel_tests/raw/DataR_CH1@DT5730_1463_hole_pulser.lh5"

#betas?
bfile = "experiment_data/betas/DataR_CH1@DT5725_1146_beta_test.lh5"
bofile = "experiment_data/betas/DataR_CH1@DT5725_1146_betas_only.lh5"
bctrlfile = "experiment_data/betas/DataR_CH1@DT5725_1146_no_beta_ctrl.lh5"
bctrlnitefile = "experiment_data/betas/DataR_CH1@DT5725_1146_no_beta_ctrl_overnight.lh5"


a_foil_file = "experiment_data/betas/DataR_CH1@DT5725_1146_alpha_foil.lh5"
b_foil_file = "experiment_data/betas/DataR_CH1@DT5725_1146_beta_foil.lh5"
both_foil_file = "experiment_data/betas/DataR_CH1@DT5725_1146_both_foil.lh5"


with h5py.File(both_foil_file, 'r+') as f:
    length = len(f["CompassEvent"]["waveform"]["dt"])
    print(f["CompassEvent"]["waveform"]["dt"][()])
    f["CompassEvent"]["waveform"]["dt"][()] = np.full(length, sample_period_2)
    print(f["CompassEvent"]["waveform"]["dt"][()])



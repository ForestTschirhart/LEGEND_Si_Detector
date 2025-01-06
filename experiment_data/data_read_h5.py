import h5py
import numpy as np
import matplotlib.pyplot as plt

### SIMPLE SCRIPT THAT READS SOME WAVEFORM DATA AND DISPLAYS IT ###



filepath1 = 'DataR_CH1@DT5730_1463_150um_roomtest_alphas.lh5'
filepath2 = 'DataR_CH1@DT5730_1463_150um_roomtest_analoghv_break.lh5'
filepath3 = 'DataR_CH1@DT5730_1463_150um_roomtest_analoghv.lh5'
filepath4 = 'DataR_CH1@DT5730_1463_150um_roomtest_dighv.lh5'
filepath5 = '../pulse_testing/DataR_CH1@DT5725_1146_air_run_1.lh5'
filepath6 = '../pulse_testing/DataR_CH1@DT5725_1146_pulser_test_2_heightmatched.lh5'

# messing around with h5py
f = h5py.File(filepath1, 'r')
g = h5py.File(filepath2, 'r')
h = h5py.File(filepath3, 'r')
i = h5py.File(filepath4, 'r')
j = h5py.File(filepath5, 'r')
k = h5py.File(filepath6, 'r')
# Access the 'CompassEvent' group
compass_event = f['CompassEvent']
compass_event2 = g['CompassEvent']
compass_event3 = h['CompassEvent']
compass_event4 = i['CompassEvent']
compass_event5 = j['CompassEvent']
compass_event6 = k['CompassEvent']

# Access the 'waveform' group within 'CompassEvent'
waveform_group = compass_event['waveform']
waveform_group2 = compass_event2['waveform']
waveform_group3 = compass_event3['waveform']
waveform_group4 = compass_event4['waveform']
waveform_group5 = compass_event5['waveform']
waveform_group6 = compass_event6['waveform']

# Access the 'values' dataset within 'waveform'
waveform_values = waveform_group['values']
waveform_values2 = waveform_group2['values']
waveform_values3 = waveform_group3['values']
waveform_values4 = waveform_group4['values']
waveform_values5 = waveform_group5['values']
waveform_values6 = waveform_group6['values']

# Read first waveform into a NumPy array (dont have to specify its a numpy array h5py does it automatically)
first_waveform = waveform_values[0, :]
first_waveform2 = waveform_values2[0, :]
first_waveform3 = waveform_values3[0, :]
first_waveform4 = waveform_values4[1, :]
first_waveform5 = waveform_values5[5, :]
first_waveform6 = waveform_values6[0, :]
time_ns = np.arange(0, len(first_waveform) * 2, 2)  # 2 ns per division
time_ns2 = np.arange(0, len(first_waveform2) * 2, 2)
time_ns3 = np.arange(0, len(first_waveform3) * 2, 2)
time_ns4 = np.arange(0, len(first_waveform4) * 2, 2)
time_ns5 = np.arange(0, len(first_waveform5) * 4, 4) # 4 ns per division
time_ns6 = np.arange(0, len(first_waveform6) * 4, 4)

# Create subplots
fig, axs = plt.subplots(6, 1, figsize=(10, 15))  # 6 rows, 1 column

# Plot each waveform in a different subplot
axs[0].plot(time_ns, first_waveform)
axs[0].set_title('alpha')
axs[0].set_xlabel('time (ns)')
axs[0].set_ylabel('ADC Amplitude')
axs[0].set_xlim(1900, 2500)

axs[1].plot(time_ns2, first_waveform2)
axs[1].set_title('analog break')
axs[1].set_xlabel('time (ns)')
axs[1].set_ylabel('ADC Amplitude')
axs[1].set_xlim(1900, 2500)

axs[2].plot(time_ns3, first_waveform3)
axs[2].set_title('analog no break')
axs[2].set_xlabel('time (ns)')
axs[2].set_ylabel('ADC Amplitude')
axs[2].set_xlim(1900, 2500)

axs[3].plot(time_ns4, first_waveform4)
axs[3].set_title('digital')
axs[3].set_xlabel('time (ns)')
axs[3].set_ylabel('ADC Amplitude')
axs[3].set_xlim(1900, 2500)

axs[4].plot(time_ns5, first_waveform5)
axs[4].set_title('old room in air')
axs[4].set_xlabel('time (ns)')
axs[4].set_ylabel('ADC Amplitude')
axs[4].set_xlim(3900, 4500)

axs[5].plot(time_ns6, first_waveform6)
axs[5].set_title('old room with scroll pump')
axs[5].set_xlabel('time (ns)')
axs[5].set_ylabel('ADC Amplitude')
axs[5].set_xlim(3900, 4500)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.subplots_adjust(hspace=0.6)

# Show the plot
plt.show()

print(np.shape(first_waveform))
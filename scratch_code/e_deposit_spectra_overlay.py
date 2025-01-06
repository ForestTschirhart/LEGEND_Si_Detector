import stop_pwr_2_deposited_E as sp2de
import nudat_crude_spectrum as ncs
import matplotlib.pyplot as plt
import numpy as np

### ATTEMPTED TO OVERLAY THE SOURCE SPECTRA FROM NUDAT_CRUDE_SPECTRUM.PY WITH THE DEPOSITED ENERGY VS INCIDENT ENERGY PLOT FROM STOP_PWR_2_DEPOSITED_E.PY
### This was sorta usefull for choosing beta source candidates

data = ncs.read_files()
ncs.format_betas(data)
ncs.format_electrons(data)
ncs.weight_Eu152(data)
print(data)

spectra = []
for source in data:
    spectrum = ncs.generate_spectra(source)
    spectra.append(spectrum)

for spectrum in spectra:
    print(spectrum[0])

# deposited energy bit
e, s_pwr = sp2de.get_data()

init_e = np.linspace(0, 2, 401)  # MeV
thickness = 0.015  # cm

deposited_energies = []
track_lengths = []
for i in range(len(init_e)):
	deposited_e, track_length, stopped = sp2de.find_deposited_energy(e, s_pwr, thickness, init_e[i])
	deposited_energies.append(deposited_e)
	track_lengths.append(track_length)


def plot_all(data, spectra, init_e, deposited_energies):
    num_spectra = len(spectra)
    # Calculate the number of rows and columns for the subplot grid
    # This example uses a simple square layout, adjust as necessary
    num_cols = int(num_spectra ** 0.5)
    num_rows = num_spectra // num_cols + (num_spectra % num_cols > 0)
    
    plt.figure(figsize=(15, 3 * num_rows))  # Adjust the figure size as needed
    
    for i, spectrum in enumerate(spectra, start=1):
        plt.subplot(num_rows, num_cols, i)
        hist_max = np.max(spectrum[:, 1])
        norm_factor = np.max(deposited_energies)/hist_max
        plt.hist(spectrum[:, 0], weights=spectrum[:, 1] * norm_factor, bins=100, alpha=0.5)  # Adjust alpha for transparency
        plt.plot(init_e * 1000, deposited_energies, label='Deposited Energy')  # Convert MeV to keV for x-axis
        plt.xlabel('Energy (keV)')
        plt.ylabel('Deposited Energy (keV)')
        plt.title(data[i-1][0] + ' Spectrum  (Activity: ' + str(data[i-1][1]) + ' uCi)')
        plt.xlim(0, 1500)
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.show()


plot_all(data, spectra, init_e, deposited_energies)

'''
#deposited_energies = np.array(deposited_energies) * 1000  # Convert MeV to keV
#deposited_max = np.max(deposited_energies)

# Normalize the deposited energies
#deposited_energies_normalized = deposited_energies * (hist_max / deposited_max)

# Plot the histogram
plt.hist(bin_centers, weights=hist /200, bins=100, alpha=0.5, label='Histogram')  # Adjust alpha for transparency
plt.xlabel('Energy (keV)')
plt.ylabel('Spectra Relative Rate, Deposited energy (keV)')

# Plot the normalized deposited energies
plt.plot(init_e * 1000, deposited_energies, label='Deposited Energy')  # Convert MeV to keV for x-axis

plt.legend()
plt.show()
'''
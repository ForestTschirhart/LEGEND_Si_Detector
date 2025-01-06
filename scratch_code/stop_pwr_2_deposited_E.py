import numpy as np
import matplotlib.pyplot as plt 

### CREATES DEPOSITED ENERGY VS INCIDENT ENERGY PLOT FOR BETAS IN SILICON ###
### Used to evaluate beta source candidates

filename = '/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project/scratch_code/estar_si.txt'
silicon_density = 2.329 #g/cm^3


def get_data():
    data_array = np.loadtxt(filename, delimiter=None, usecols=(0, 3), skiprows=9)
    e_tmp = data_array[:, 0]
    s_pwr_tmp = silicon_density * data_array[:, 1] #convert from MeV cm^2/g to MeV/cm
    e = np.linspace(1E-2, 1E3, 399997)
    s_pwr = np.interp(e, e_tmp, s_pwr_tmp)
    return e, s_pwr


def find_start_index(e, init_e):
    for i in range(len(e)):
        if e[i] >= init_e:
            if (init_e - e[i-1]) < (e[i] - init_e):
                return i-1
            else:
                return i


def find_deposited_energy(e, s_pwr, thickness, init_e):
    i = find_start_index(e, init_e)
    deposited_e = 0
    track_length = 0
    stopped = False
    while (track_length < thickness) & (i > 0):
        delta_e = e[i] - e[i-1]
        dl = 2 * delta_e / (s_pwr[i-1] + s_pwr[i])
        track_length += dl
        deposited_e += delta_e

        #print(i, deposited_e, track_length, dl)

        if i-1 == 0:
            stopped = True
        i -= 1
    return deposited_e, track_length, stopped

def graph_tracklengths(init_e, track_lengths):
    plt.plot(init_e, track_lengths)
    plt.xlabel('Initial Energy (MeV)', fontsize=15)
    plt.ylabel('Track Length (cm)', fontsize=15)
    plt.title('Track Length vs Initial Energy in 150 microns of Si', fontsize=15)
    plt.show()



if __name__ == '__main__':
    e, s_pwr = get_data()

    init_e = np.linspace(0,16,401)  #MeV
    thicknesses = [0.004, 0.015, 0.1] #cm

    figures = []
    for thickness in thicknesses:
        deposited_energies = []
        track_lengths = []
        for i in range(len(init_e)):
            deposited_e, track_length, stopped = find_deposited_energy(e, s_pwr, thickness, init_e[i])
            deposited_energies.append(deposited_e)
            track_lengths.append(track_length)
        figures.append(deposited_energies)

    num_figs = len(figures)
    # Calculate the number of rows and columns for the subplot grid
    # This example uses a simple square layout, adjust as necessary
    num_cols = int(num_figs ** 0.5)
    num_rows = num_figs // num_cols + (num_figs % num_cols > 0)



    plt.figure(figsize=(8, 5.5))  # Adjust the figure size as needed

    for i, figure in enumerate(figures, start=1):

        plt.plot(init_e, figure, label='Detector Thickness: ' + str(int(round(thicknesses[i-1]*10000,0))) + ' micron')  # Adjust alpha for transparency
        plt.xlabel('Initial Energy (MeV)')
        plt.ylabel('Deposited energy (MeV)')
        plt.xlim(-0.25, 10)
        #plt.xscale('log')
        #plt.yscale('log')
        plt.grid(which='both')

    plt.suptitle('Deposited Energy vs. Initial Energy of Betas in Silicon', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.subplots_adjust(top=0.90)
    plt.legend()
    plt.show()

    #graph_tracklengths(init_e, track_lengths)


    print(deposited_e, track_length, stopped)

            
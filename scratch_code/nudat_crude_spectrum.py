import numpy as np
import re
import matplotlib.pyplot as plt

### GENERATES A REALLY CRUDE "SPECTRUM" FROM NUDAT DATA ###
### Used to evaluate Beta source candidates


input_file_paths = ['scratch_code/nudat_data/Al26.txt', 'scratch_code/nudat_data/Bi207.txt', 'scratch_code/nudat_data/Cs137.txt', 'scratch_code/nudat_data/Eu152.txt', 'scratch_code/nudat_data/Sr90.txt', 'scratch_code/nudat_data/Y90.txt']
CENPA_isotopes = [['Al26', 0, 0.003], ['Bi207', 1, 1], ['Cs137', 2, 10.82], ['Cs137', 2, 1.06], ['Cs137', 2, 87.66], ['Cs137', 2, 0.071], ['Eu152', 3, 105], ['Eu152', 3, 10], ['Sr90', 4, 105], ['Y90', 5, 105]]
#output_file_paths = 'scratch_code/nudat_table_processed.txt'


def read_files():
    data = []
    for triple in CENPA_isotopes:
        betas = []
        electrons = []
        reading_betas = False
        reading_electrons = False

        with open(input_file_paths[triple[1]], 'r') as file:
            for line in file:
                # Check for the section markers
                if 'Betas:' in line:
                    reading_betas = True
                    reading_electrons = False
                    continue  # Skip the marker line
                elif 'Electrons:' in line:
                    reading_betas = False
                    reading_electrons = True
                    continue  # Skip the marker line
                
                # Based on the current section, append the line to the respective list
                if reading_betas and line.strip():
                    betas.append(line.strip())
                elif reading_electrons and line.strip():
                    electrons.append(line.strip())

        data.append([triple[0], triple[2], betas, electrons])
    return data


def format_betas(data):
    for source_idx, source in enumerate(data):
        for line_idx, line in enumerate(source[2]):
            placeholder = "|||"  # Unique placeholder for multiple spaces
            line_with_placeholder = re.sub(r'\s{2,}', placeholder, line)
            line_no_single_spaces = line_with_placeholder.replace(" ", "")
            final_line = line_no_single_spaces.replace(placeholder, " ")
            columns = final_line.split()
            without_second_column = ' '.join(columns[:1] + columns[2:])
            without_percentage = without_second_column.split('%')[0]  # Keep everything before '%'
            without_percentage_split = without_percentage.split()
            e_i = [float(without_percentage_split[0]), float(without_percentage_split[1])]
            data[source_idx][2][line_idx] = e_i # Assign modified line back
        data[source_idx][2] = np.array(data[source_idx][2])


def format_electrons(data):
    for source_idx, source in enumerate(data):
        for line_idx, line in enumerate(source[3]):
            placeholder = "|||"  # Unique placeholder for multiple spaces
            line_with_placeholder = re.sub(r'\s{2,}', placeholder, line)
            line_no_single_spaces = line_with_placeholder.replace(" ", "")
            final_line = line_no_single_spaces.replace(placeholder, " ")
            columns = final_line.split()
            without_first_column = ' '.join(columns[1:])  # Remove the first column
            without_percentage = without_first_column.split('%')[0]  # Keep everything before '%'
            without_percentage_split = without_percentage.split()
            e_i = [float(without_percentage_split[0]), float(without_percentage_split[1])]
            data[source_idx][3][line_idx] = e_i  # Assign modified line back
        data[source_idx][3] = np.array(data[source_idx][3])


# Eu152 has 2 decay modes from the ground state, with different percentages of occuring
def weight_Eu152(data):
    for source in data[6:8]:
        source[2][0:12, 1] *= 0.2792
        source[2][12:, 1] *= 0.7208
        source[3][0:213, 1] *= 0.2792
        source[3][213:, 1] *= 0.7208
           

# add beta and electron data together to get the total spectrum, then multiply by source activity
def generate_spectra(source):
    activity = source[1]
    betas = source[2]
    electrons = source[3]

    if source[0] == 'Sr90':
        total_spectrum = betas
    else:
        total_spectrum = np.concatenate((betas, electrons))

    total_spectrum[:, 1] *= activity
    total_spectrum[:, 1] *= .37 # uCi --> kBq     1 uCi = 37 kBq, divided by 100 to turn percents into factors
    return total_spectrum
        

def plot_spectra(data, spectra):
    num_spectra = len(spectra)
    # Calculate the number of rows and columns for the subplot grid
    # This example uses a simple square layout, adjust as necessary
    num_cols = int(num_spectra ** 0.5)
    num_rows = num_spectra // num_cols + (num_spectra % num_cols > 0)
    
    plt.figure(figsize=(15, 3 * num_rows))  # Adjust the figure size as needed
    
    for i, spectrum in enumerate(spectra, start=1):
        plt.subplot(num_rows, num_cols, i)
        plt.hist(spectrum[:, 0], weights=spectrum[:, 1], bins=100, alpha=0.5)  # Adjust alpha for transparency
        plt.xlabel('Energy (keV)')
        plt.ylabel('Rate (kBq)')
        plt.title(data[i-1][0] + ' Spectrum  (Activity: ' + str(data[i-1][1]) + ' uCi)')
    
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.show()



if __name__ == '__main__':
    data = read_files()
    format_betas(data)
    format_electrons(data)
    weight_Eu152(data)

    spectra = []
    for source in data:
        spectrum = generate_spectra(source)
        spectra.append(spectrum)

    for spectrum in spectra:
        print(spectrum[0])

    plot_spectra(data, spectra)


#print(data[6][2])
#print(data[6][3][211:215])
#print(data[0])

# IDEAAA take all the nudat data and put them into a directory of a bunch of files, then do this for all those files and for an array of all [[isotope, activities]]
# then for each output array of real_E_and_rate, save it to a file in another directory
# THEN graph all of the arrays in histograms of rate vs energy and this will give you a good idea of which sources have the most weird stuff going on

# want to avoid 
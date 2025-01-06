import numpy as np
import re

### TOOL FOR FINDING RELEVANT EMISSIONS FROM NUDAT DATA TABLES ###
### Some Nudat data tables are full of negligible emiisions, this tool can help you cut those and organize by intensity

input_file_path = 'scratch_code/nudat_table_temp.txt'
output_file_path = 'scratch_code/nudat_table_processed.txt'


# cleaning up the data
def process_line(line):
    placeholder = "|||"  # Unique placeholder for multiple spaces
    line_with_placeholder = re.sub(r'\s{2,}', placeholder, line)
    line_no_single_spaces = line_with_placeholder.replace(" ", "")
    final_line = line_no_single_spaces.replace(placeholder, " ")
    columns = final_line.split()
    without_first_column = ' '.join(columns[1:])  # Remove the first column
    without_percentage = without_first_column.split('%')[0]  # Keep everything before '%'
    return without_percentage


with open(input_file_path, 'r') as file:
    lines = file.readlines()

processed_lines = [process_line(line) for line in lines]

with open(output_file_path, 'w') as file:
    for line in processed_lines:
        file.write(f"{line}\n")

# Replace 'your_file.txt' with the path to your text file

# If your data is separated by commas, for example, use delimiter=','
data_array = np.loadtxt(output_file_path, delimiter=None, usecols=(0, 1))

# Sort data_array in descending order by the second column
indices_desc = np.argsort(data_array[:, 1])[::-1]  # Get indices for sorting in descending order
sorted_data_array = data_array[indices_desc]

print(sorted_data_array)

# Filter out rows where the first column is less than 300
filtered_data_array = sorted_data_array[sorted_data_array[:, 0] >= 300]

#print(filtered_data_array)

# Round elements in filtered_data_array to the first decimal place
rounded_data_array = np.around(filtered_data_array, decimals=1)

#print(rounded_data_array)

# Print rounded_data_array without unnecessary trailing zeros
'''for row in rounded_data_array:
    print(f"{row[0]:.1f}    {row[1]:.1f}")
'''


def activity_x_intensity(sorted_data_array, activity, solid_angle_percent=1):
    #rows, cols = sorted_data_array.shape
    real_E_and_rate = sorted_data_array
    real_E_and_rate[:, 1] *= activity/100*37000*solid_angle_percent
    return real_E_and_rate


real_E_and_rate = activity_x_intensity(sorted_data_array, 23.69)
print(real_E_and_rate)




# IDEAAA take all the nudat data and put them into a directory of a bunch of files, then do this for all those files and for an array of all [[isotope, activities]]
# then for each output array of real_E_and_rate, save it to a file in another directory
# THEN graph all of the arrays in histograms of rate vs energy and this will give you a good idea of which sources have the most weird stuff going on


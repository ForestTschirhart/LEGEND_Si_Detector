import h5py
import numpy as np
import matplotlib.pyplot as plt
import lgdo 

### SCRIPT THAT HELPS VISUALIZE THE STRUCTURE OF AN H5 FILE ###

#lgdo.lh5.tools.show('experiment_data/DataR_CH1@DT5725_1146_run_2.lh5', attrs=True, detail=True)
filea = 'experiment_data/betas/DataR_CH1@DT5725_1146_alpha_foil.lh5'
fileb = 'experiment_data/betas/DataR_CH1@DT5725_1146_beta_foil.lh5'
filec = 'experiment_data/betas/DataR_CH1@DT5725_1146_no_beta_ctrl_overnight.lh5'


# messing around with h5py
f = h5py.File(filec, 'r+')

# Function to recursively list the contents of a group
def list_contents(group, indent=0):
    for key, item in group.items():
        print('  ' * indent + key)
        if isinstance(item, h5py.Group):
            list_contents(item, indent + 1)
        elif isinstance(item, h5py.Dataset):
            # For datasets, you might want to print their shape or dtype
            print('  ' * (indent + 1) + f"Dataset with shape {item.shape}, dtype {item.dtype}")
            print(item[:])

# List top-level groups and datasets
print("Top-level contents:")
list_contents(f)



# Inspect attributes of the root group
print("\nAttributes of the root group:")
for name, value in f.attrs.items():
    print(f"{name}: {value}")


# Example: Reading data from a dataset (assuming 'some_dataset' is a path to a dataset)
# dataset_path = 'path/to/some_dataset'
# data = f[dataset_path][()]
# print(data)

# Don't forget to close the file when you're done
f.close()


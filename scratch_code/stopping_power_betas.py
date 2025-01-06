import numpy as np
import matplotlib.pyplot as plt 

### MAKES GRAPH OF STOPPING POWER OF SILICON FOR BETAS ###

filename = '/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project/scratch_code/estar_si.txt'

data_array = np.loadtxt(filename, delimiter=None, usecols=(0, 3), skiprows=9)
x = data_array[:, 0]
y = data_array[:, 1]

x_cut2 = x[:37]
y_cut2 = y[:37]

x_cut10 = x[:49]
y_cut10 = y[:49]
#plt.plot(x_cut2, y_cut2)
plt.plot(x_cut10, y_cut10)
#plt.plot(x, y)
plt.xlabel('Energy (MeV)', fontsize=15)
plt.ylabel('Stopping Power (MeV cm^2/g)', fontsize=15)
plt.title('Stopping Power of Silicon for Betas', fontsize=15)
#plt.yscale('log')
#plt.xscale('log')
#plt.axhline(y=2, color='r', linestyle='--')
plt.show()

print(x_cut10)
#print(x_cut2)

'''
print(data_array.shape)
print(data_array)
print(x)
print(x.shape)
'''
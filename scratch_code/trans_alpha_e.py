import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from scipy import stats
from numpy import asarray as ar, exp, sqrt


### ANALYSES TRANSMITTED ALPHA DATA FROM SRIM SIMULATION ###
### Used when thinking about degradation foil thickness

# Source emits 5.486 MeV alphas 
alpha_energy = 5.486 


# Reads the file and returns an array of the energy of every transmitted alpha in MeV
def generate_data(path, rows=100, cols=(3)):

    trimdata = open(path)
    
    data_array = np.loadtxt(trimdata, skiprows=12,max_rows=rows, usecols=cols)
    # eV ---> MeV
    data_array = data_array / 1000000

    trimdata.close()

    return data_array


# Gaussian function
def gaus(x,a,mu,sigma):
    return a*exp(-(x-mu)**2/(2*sigma**2))


# Graphs the energy of the transmitted alphas 3 ways: Histogram, Fitted Gaussian, Calculated Gaussian 
def graphTransEnergy(data):

    binedges = np.linspace(.5,1.5,101)
    binwidth = (binedges[1] - binedges[0])
    hist = np.histogram(data, bins=binedges, density=False)[0]
    bincenters = binedges[0:-1] + (binedges[1] - binedges[0])/2.0

    print(binwidth)

    n = len(data)
    brute_mean= np.sum(hist*bincenters)/n
    brute_sigma = np.sqrt(np.sum(hist*(bincenters-brute_mean)**2)/n)
    brute_mean01 = np.mean(data)
    brute_sigma01 = np.std(data)

    print("Brute forced mean and sigma w/ numpy: ", brute_mean01, brute_sigma01)
    
    print("Brute forced mean and sigma: ", brute_mean, brute_sigma)

    sigmas = np.sqrt(hist)

    popt,pcov = curve_fit(gaus,bincenters,hist, sigma = sigmas,absolute_sigma=True)

    print(popt[0])
    print(n/(brute_sigma*sqrt(2*3.1415)))
    fancy_mean = popt[1]
    fancy_sigma = popt[2]
    print("Fancy mean and sigma: ", fancy_mean, fancy_sigma)

    plt.scatter(bincenters, hist, clip_on=False, label='Data')
    plt.plot(bincenters, gaus(bincenters,popt[0],popt[1],popt[2]), color='crimson', label='Fitted function')

    # trying to get this to work but it won't
    plt.plot(bincenters, gaus(bincenters,binwidth*n/(brute_sigma*sqrt(2*3.1415)),brute_mean,brute_sigma), color='green', label='Calculated function')

    plt.title('Energy of Alpha Particles Transmitted Through Titanium')
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Counts')
    plt.legend(loc='best')
    plt.margins(x=0)
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.show()




data = generate_data('/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project/scratch_code/TRANSMIT.txt', rows = None)
print(data)
graphTransEnergy(data)

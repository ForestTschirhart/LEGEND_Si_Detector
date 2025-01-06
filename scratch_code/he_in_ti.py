import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import RectBivariateSpline, CloughTocher2DInterpolator, RegularGridInterpolator
import itertools
from scipy.optimize import curve_fit, minimize
from scipy import stats

### NOT SURE WHAT THIS IS ###
### Upladed for completeness

def main():	

	alphaEnergy = 3271.0
	thickness = 10000

	material = 'Ti'

	# find number of events in the file (12 header lines)
	numEvents = 34663

	# open file with transmitted ion data
	trimdata = open('/home/lv/Documents/anl/quick_srims/TRANSMIT.txt')

	# ignore header info
	for i in range(0,12):
		trimdata.readline()

	# import data (only need energy information)
	#energies = np.zeros((numEvents))
	energies = []
	for i in range(0,numEvents-2):
		columns = trimdata.readline().strip().split()
		if (float(columns[6]) > 0.99):
			energies.append( (alphaEnergy * 1000.0 - float(columns[2]))/1000.0)

	# close the file
	trimdata.close()

	binedges = np.linspace(0,3000,3001)

	hist = np.histogram(energies, bins=binedges, density=False)[0]

	bincenters = binedges[0:-1] + (binedges[1] - binedges[0])/2.0
	
	guessmean = np.average(energies)
	guesssd =  np.sqrt(2 * np.var(energies))
	initparams = [guessmean, guesssd]

	b=2.0

	results = minimize(mlfunc_gennorm, initparams, args=(bincenters, hist, b), method='Nelder-Mead')

	u = results.x[0]
	sd = results.x[1]

	print(u, sd)

	pred = np.sum(hist) * (bincenters[1] - bincenters[0]) * stats.gennorm.pdf(bincenters, b, loc=u, scale=sd)

	plt.figure()
	plt.plot(bincenters, hist, 'k.')
	plt.plot(bincenters, pred, label='gennorm fit, b=%0.2f'%b)
	plt.xlabel('energy loss (keV)')
	plt.ylabel('counts')
	plt.title('TRIM sim. %i keV alpha through %i nm '%(alphaEnergy, thickness)+material)
	plt.legend()
	plt.show()

	return

def mlfunc_gennorm(params, bincenters, hist, b):
	u = params[0]  # mean
	sd = params[1]	# approx standard deviation (if it were actually a normal distribution with beta=2)

	pred = np.sum(hist) * (bincenters[1] - bincenters[0]) * stats.gennorm.pdf(bincenters, b, loc=u, scale=sd)

	ll = -2.0 * np.sum(stats.poisson.logpmf(hist, pred))

	return ll

main()
import h5py
from dspeed import build_dsp
import numpy as np
import matplotlib.pyplot as plt

### BARE BONES SCIPRT THAT DOES SOME DSP ON A FILE AND PLOTS THE RESULTS ###
### Intended to be called from terminal from many different locations, giving quick data visualization



file = "DataR_CH1@DT5730_1463_500um_random_signals.lh5" # path to raw file
dsp_file = "DataR_CH1@DT5730_1463_500um_random_signals_dsp.lh5" # path to output dsp file

dsp_config = {
    "outputs": ["bl", "trapEftp", "wf_pz", "wf_blsub", "wf_etrap"],
    "processors": {
        "bl, bl_sig, bl_slope, bl_intercept": {
            "function": "linear_slope_fit",
            "module": "dspeed.processors",
            "args": ["waveform[:1000]", "bl", "bl_sig", "bl_slope", "bl_intercept"],
            "unit": ["ADC", "ADC", "ADC", "ADC"]
        },
        "wf_blsub": {
                "function": "subtract",
                "module": "numpy",
                "args": ["waveform", "bl", "wf_blsub"],
                "unit": "ADC"
            },
        "wf_pz": {
                "function": "pole_zero",
                "module": "dspeed.processors",
                "args": ["wf_blsub", "db.pz_tau", "wf_pz"],
                "unit": "ADC"
            },
        "wf_etrap": {
                "function": "trap_norm",
                "module": "dspeed.processors",
                "args": ["wf_pz", "db.etrap.rise", "db.etrap.flat", "wf_etrap"],
                "unit": "ADC"
            },
        "trapEftp": {
                "function": "fixed_time_pickoff",
                "module": "dspeed.processors",
                "args": ["wf_etrap", "db.ftp", "'l'", "trapEftp"], 
                "unit": "ADC"
            }
    }    
}

rise = 3.8
flat = 0.1

dsp_db = {
    "CompassEvent": {
        "pz_tau": "1*ms",
        "etrap": {
            "rise": f"{rise}*us",
            "flat": f"{flat}*us"
        },
        "ftp": 1000 + (rise + 0.5*flat)/(0.002)    
    }
}


build_dsp(
    f_raw=file, 
    f_dsp=dsp_file,
    lh5_tables = "CompassEvent",
    dsp_config = dsp_config,
    database = dsp_db,
    write_mode = 'r'
)


filechoice = dsp_file
f = h5py.File(filechoice)
trapEftp = f['CompassEvent']['trapEftp']
trap_data = trapEftp


def select_n_cut(trap_data, cut=False):
    if cut:
        noise_cut = trap_data[:]
        noise_cut = noise_cut[noise_cut > 500]
    else:
        noise_cut = trap_data[:]
    return noise_cut


def gaussian(x, A, mean, std):
    return A * np.exp(-1. * ((x-mean)**2.)/(2. * std**2))


data = select_n_cut(trap_data)
bins = np.linspace(0, 2000, 2001)
counts, _ = np.histogram(data, bins=bins)

a = np.max(counts)
mean = np.mean(data)
std = np.std(data)
fwhm = 2.355*std

gaussian_fit = gaussian(bins, a, mean, std)

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.hist(data, bins=bins, color='blue')
ax1.plot(gaussian_fit)
ax1.axvline(mean, color='black', linestyle='--', label='Mean: ' + str(round(mean, 2)))
ax1.axvline(mean + fwhm/2, color='black', linestyle=':', label='FWHM: ' + str(round(fwhm, 2)))
ax1.axvline(mean - fwhm/2, color='black', linestyle=':')
ax1.set_ylabel("counts")
ax1.set_xlabel("adc")
ax1.set_title(f'Pulse Test Spectrum [Rise: {rise}us, Flat: {flat}us]')
#ax1.xlim(350,650)
#ax1.xlim(525, 575)
#ax1.xlim(460,760)
ax1.legend()


print(a, mean, std, fwhm)

bl = f['CompassEvent']['bl']
wf_blsub = f['CompassEvent']['wf_blsub']['values']
wf_pz = f['CompassEvent']['wf_pz']['values']
wf_etrap = f['CompassEvent']['wf_etrap']['values']

super_bl = np.average(bl/np.max(bl))
super_wf_blsub = np.average(wf_blsub/np.max(wf_blsub, axis=1)[:,None], axis=0)
super_wf_pz = np.average(wf_pz/np.max(wf_pz, axis=1)[:,None], axis=0)
super_wf_etrap = np.average(wf_etrap/np.max(wf_etrap, axis=1)[:,None], axis=0)


#ax2.figure(figsize=(12,10))
ax2.axhline(super_bl, label="bl")
ax2.plot(super_wf_blsub, label="original");
ax2.plot(super_wf_pz, label="pz corrected");
ax2.plot(super_wf_etrap, label="etrap");
ax2.axvline(dsp_db["CompassEvent"]["ftp"], label="ftp");
ax2.axhline(0.85, color='black', linestyle='--')
ax2.set_xlabel("time [ns]")
ax2.set_ylabel("normalized adc")
ax2.legend()
#ax2.xlim(1000, 1500)

plt.show()


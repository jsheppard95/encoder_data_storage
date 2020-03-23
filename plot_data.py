"""
plot_data.pu

Module to read/plot data files generated by enc_data_storage.py
"""

import matplotlib.pyplot as plt
import numpy as np

INFILE_NAME = 'm1k4_pitch.csv'


def fftplot(x_axis, y_axis,
            xlabel=None, left_label='FFT Amplitude',
            remove_dc=True, scale=1.0, alpha=0.7):
    step_x = x_axis[1] - x_axis[0]
    freqs = np.fft.rfftfreq(len(x_axis), step_x)
    fft = np.fft.rfft(x_axis)
    spectra = np.abs(fft) / len(fft)

    # Remove DC component
    if remove_dc:
        data = spectra[1:]
        x_axis = freqs[1:]
    else:
        data = spectra
        x_axis = freqs

    if xlabel is None:
        xlabel = 'Frequency [Hz]'

    f, ax = plt.subplots()
    ax.plot(x_axis, data, alpha=alpha)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(left_label)
    ax.set_xlim(min(x_axis), max(x_axis))
    f.show()


tvals = []
enc_vals = []
with open(INFILE_NAME, 'r') as infile:
    for line in infile:
        line_list = line.split(',')
        tvals.append(float(line_list[0]))
        enc_vals.append(float(line_list[1]))

print('Siganl Duration: %s s' % str(tvals[-1] - tvals[0]))

# Plot Position vs Time:
f, ax = plt.subplots()
ax.plot(tvals, enc_vals)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Position')
ax.grid(True)
f.show()

# Plot Spectrum
fftplot(tvals, enc_vals)

input('Press <Enter> to close')

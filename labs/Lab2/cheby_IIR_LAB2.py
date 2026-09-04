#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 16:17:44 2026

@author: villani
"""

from scipy.signal import iirdesign, freqz
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.ticker

# --- Plantilla ---
fpass = 100         # Hz
fstop = 300         # Hz
ripple = 1          # dB, atenuación máxima en banda de paso (alpha_max)
attenuation = 60    # dB, atenuación mínima en banda de rechazo (alpha_min)

fsamp = 20000  # Hz, frecuencia de muestreo

system = iirdesign(
    wp=fpass,
    ws=fstop,
    gpass=ripple,
    gstop=attenuation,
    analog=False,
    ftype='cheby1',
    output='ba',
    fs=fsamp
)
print(system)
# print("b =", b)
# print("a =", a)

# system = signal.iirdesign(wp, ws, gpass, gstop)
w, h = signal.freqz(*system, fs=fsamp)

fig, ax1 = plt.subplots()
ax1.set_title('Digital filter frequency response')
ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Amplitude [dB]', color='b')
ax1.set_xlabel('Frequency [rad/sample]')
ax1.grid(True)
ax1.set_ylim([-120, 20])
ax2 = ax1.twinx()
phase = np.unwrap(np.angle(h))
ax2.plot(w, phase, 'g')
ax2.set_ylabel('Phase [rad]', color='g')
ax2.grid(True)
ax2.axis('tight')
ax2.set_ylim([-6, 1])
nticks = 8
ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
ax2.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))

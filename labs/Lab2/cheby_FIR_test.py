#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:32:34 2026

@author: villani
"""

import sympy as sp
import numpy as np
import scipy.signal as sig
from scipy.signal.windows import hamming, kaiser, blackmanharris
import matplotlib.pyplot as plt

from pytc2.sistemas_lineales import plot_plantilla, group_delay

# frecuencia de muestreo normalizada
fs = 20*10**3
# tamaño de la respuesta al impulso
cant_coef = 151

filter_type = 'lowpass'

fpass = 100 # 
ripple = 1 # dB
fstop = 300 # Hz
attenuation = 60 # dB

f_predist = 60  #Hz

# construyo la plantilla de requerimientos
frecs = [0.0,  fpass + f_predist,   fstop - f_predist ,   fs/2]
gains = [0,   -ripple, -attenuation,   -np.inf] # dB

gains = 10**(np.array(gains)/20)


# FIR design
#num_bh = sig.firwin2(cant_coef, frecs, gains , window='blackmanharris' , 1000)
num_hm = sig.firwin2(cant_coef, frecs, gains , window='hamming', fs=fs)
#num_ka = sig.firwin2(cant_coef, frecs, gains , window=('kaiser',14) , fs=f1/2
                     
den = 1.0



def plot_freq_resp_fir(this_num, this_desc):

    wrad, hh = sig.freqz(this_num, 1.0)
    ww = wrad / np.pi
    
    plt.figure(1)

    plt.plot(ww, 20 * np.log10(abs(hh)), label=this_desc)

    plt.title('FIR diseñado por métodos directos - Taps:' + str(cant_coef) )
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Modulo [dB]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()
    
    plt.figure(2)

    phase = np.unwrap(np.angle(hh))

    plt.plot(ww, phase, label=this_desc)

    plt.title('FIR diseñado por métodos directos - Taps:' + str(cant_coef))
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Fase [rad]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()

    plt.figure(3)

    # ojo al escalar Omega y luego calcular la derivada.
    gd_win = group_delay(wrad, phase)

    plt.plot(ww, gd_win, label=this_desc)

    plt.ylim((np.min(gd_win[2:-2])-1, np.max(gd_win[2:-2])+1))
    plt.title('FIR diseñado por métodos directos - Taps:' + str(cant_coef))
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Retardo [# muestras]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()    

plt.close('all')

#plot_freq_resp_fir(num_bh, filter_type+ '-blackmanharris')    
plot_freq_resp_fir(num_hm, filter_type+ '-hamming')    
#plot_freq_resp_fir(num_ka, filter_type+ '-kaiser-b14')    
    
    
# sobreimprimimos la plantilla del filtro requerido para mejorar la visualización    
fig = plt.figure(1)    
plot_plantilla(filter_type = filter_type , fpass = fpass/(fs/2), ripple = ripple , fstop = fstop/(fs/2), attenuation = attenuation, fs = fs)
ax = plt.gca()
ax.legend()

# reordenamos las figuras en el orden habitual: módulo-fase-retardo
plt.figure(2)    
axes_hdl = plt.gca()
axes_hdl.legend()

plt.figure(3)    
axes_hdl = plt.gca()
axes_hdl.legend()

print(num_hm)

plt.show()
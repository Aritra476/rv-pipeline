import numpy as np
import matplotlib.pyplot as plt

# basic parameters
N = 500
dx = 0.01
x = np.arange(N)*dx    # range of x from 0 to N*dx

freq = np.fft.fftshift(np.fft.fftfreq(N, d= dx))

'''
^the fft frequency decide the diff between two consecutive freq through the whole array by:

fk = k/N.dx
fk = 1/0.01*500 = 0.2

the max range in which the fft produce freq is called nyquist freq :

f = 1/2*dx 
f = 1/2*0.01 = 50 so the range is form -50 to 50 
 
^to make the frequency without fft and check with the fft freq 

freq1 = np.round(np.arange(-50,50,0.2),1)

freqm = np.round(freq - freq1,5)

print(f"x = {x, x.shape} | freq = {freq, freq.shape} | freq1 = {freq1, freq1.shape}| freqm = {freqm, freqm.shape}")

assert np.allclose(freq,freq1) , "frequency don't match by different methods"
'''
# building a signal : two sinusoids
f1 ,f2 = 5.0, 23.0
y= np.sin(2*np.pi*f1*x) + 0.5*np.sin(2*np.pi*f2*x)



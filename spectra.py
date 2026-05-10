import numpy as np


def Gaussian_line(wav,wav0,sigma,amp):
    wav0 = np.asarray(wav0)
    wav  = np.asarray(wav)
    if wav0.ndim == 0:
        result =  amp*np.exp(-(wav - wav0)**2 / (2 * sigma**2))
        return result
    
    else:
        result = amp * np.exp(-(wav[:, np.newaxis] - wav0[np.newaxis, :])**2 / (2 * sigma**2))
        return result
    

if __name__ == "__main__":

    wav = np.linspace(4990,5010,1000)
    wav0 = 5000.0
    wav0 = np.array([5000,5000.50,5010,5012])
    sigma = 1.0
    amp = 1.0

    profile = Gaussian_line(wav,wav0,sigma,amp)
    print(profile)
import numpy as np
import matplotlib.pyplot as plt

wav = np.linspace(4990,5010,1000)
wav0 = 5000
sigma = 2.0
amp = 1.0
depth = 0.7

# as close to Normalized flux it can be 
def flux(wav,wav0,sigma,amp):
    x = 1 - depth*(amp*np.exp(-(wav-wav0)**2/(2*sigma**2)))
    return x

flux = np.asarray(flux(wav,wav0,sigma,amp))

def add_noise (flux,snr,read_noise = 3.0 ,seed = None):

    #add noise to the synthetic spectrum
    # 
    # parameters:
    # flux : find using the equation
    #       amp*np.exp(-(wav-wav0)**2/(2*sigma**2))    
    # 
    # snr  : a float value 
    #       Signal to noise ratio at flux = 1
    #
    # read_noise : noise of measuring a single photon sue to CCD (kept at 3 electrons fro typical ones)
    # 
    # seed : random seed for having reproducibility kept at random
    # 
    # Output:
    #  flux_noisy = flux with both poisson (photon noise) and Gaussian  (detector noise)
    # 
    # Equations :
    #  (for converting the flux into photon counts)
    #  1. N(lambda) = flux(lambda) * snr**2
    #  2. for poisson noise using rng.poisson (clipping the N_photon to be greater than 0 with no upper bound with maintaining its dtype)
    #  3. for gaussian noise using rng.normal(0.0 because gaussian line center,read_noise of detector,and size of the flux)
    #  4. for flux_noisy = N_obs / snr**2 to convert it back to flux from photon counts
    
    # new np.random 
    rng = np.random.default_rng(seed = seed)

    #convert normalized flux to photon count
    N_photon = flux * (snr**2) 

    #poisson noise
    #clip to 0 to avoid negative input (it can happen in deep line)
    #  it require float input so astype(float)
    N_obs = rng.poisson(np.clip(N_photon,0,None).astype(float))

    # gaussian noise
    N_obs = N_obs + rng.normal(0.0,read_noise,size=flux.shape)

#   converting back to flux from photon counts
    flux_noisy = N_obs / snr**2

    return flux_noisy

if __name__ == '__main__':

    snr = 100.0

    flux_noisy = add_noise (flux,snr,read_noise = 3.0 ,seed = None)

# the change in SNR comes from that the SNR 100 is total for continuum where flux is greater than 1
# when we measured snr it measure from the whole spectrum including absorption lines 
# where photons count is low than continuum so the snr falls and noise has also some effects
# fro that we normalized the flux
# using the continuum mask so that we take only flux near 1 so the snr don't fluctuate crazy

    mask = flux > 0.8
    noisy = add_noise (flux[mask],snr,read_noise = 3.0 ,seed = None)
    mean_flux = (noisy - flux[mask])
    measured_snr = 1 / np.std(noisy - flux[mask])
    print(f"expected and measured is (with mask)= {snr,measured_snr}")


# to see the noise
    fig,ax = plt.subplots(figsize=(10,10))
    ax.plot(wav,flux,'b--',linewidth = 2.5,label = 'normal')
    ax.plot(wav,flux_noisy,'r--',linewidth = 1.5,label = 'noise')
    ax.axhline(1,linestyle='--',color= 'black',linewidth=1.0)
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('FLux')
    ax.set_title('with and without noise flux ')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# for different values for snr 
# using the continuum mask so that we take only flux near 1 so the snr don't fluctuate crazy


    for snr in [10,50,100,300,500]:
        
        mask = flux > 0.8
        noisy = add_noise (flux[mask],snr,read_noise = 3.0 ,seed = None)
        mean_flux = (noisy - flux[mask])
        measured_snr = 1 / np.std(noisy - flux[mask])
        print(f"expected and measured is = {snr,measured_snr}")
        assert abs(measured_snr - snr)  / snr < 0.1 , "SNR off by greater than 10 percentage" 
    print("passed")


    



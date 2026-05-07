# adding doppler broadening to ery wavelength depending on the velocity 
# lambda_obs = lambda_0 * (1 + v/c)


import numpy as np
from astropy import constants as const

c1 = const.c.to("km/s").value
wav = np.array([5000,5005,5010])

def doppler_C(wav,v_t):
    B = v_t/c1
    wav0  = wav*(1+B)
    return wav0

def doppler_r(wav,v_t):
    B = v_t/c1
    wav0 = wav*(np.sqrt((1 + B)/( 1 - B)))
    return wav0

if __name__ == '__main__' :
    wav = np.linspace(5000,5010,1000)
    v_t = 45 # km/s

    shifted_c = doppler_C(wav,v_t)
    shifted_r = doppler_r(wav,v_t)

    # positive v_r is receding
    assert np.all(shifted_c > wav), "v_r > 0 gives red shift"
    assert np.all(shifted_r > wav), "v_c > 0 must give redshift"

    #negative v_r is blue shift
    assert np.all(doppler_C(wav,-45) < wav),"classical blue shift failed "
    assert np.all(doppler_r(wav,-45) < wav),"relativistic blue shift failed"

    # v = 0 wav = shifted
    assert np.allclose(doppler_C(wav,0.0),wav),"zero velocity failed"
    assert np.allclose(doppler_r(wav,0.0),wav),"zero velocity failed"

    #difference
    diff = np.mean(np.abs(shifted_r-shifted_c))/wav.mean()*const.c.to('m/s').value
    print(f"classical vs relativistic difference at 45 km/s = {diff:.4f}m/s")
    assert diff < 5.0 ,"difference too large "

    print("all test passed")







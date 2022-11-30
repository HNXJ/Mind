import numpy as np
import scipy


def psdt(y, fs, timeBins=10, freqBins=10): # JUST A TEST
    
    psd_ = np.zeros([timeBins, freqBins])
    w = np.floor(y.shape[0] / timeBins)
    for i in range(timeBins):
        
        x = y[i*w:(i+1)*w]
        f = 1
    
    return 0
    
    
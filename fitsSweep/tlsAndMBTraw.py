import numpy as np
from scipy.special import digamma
import scipy.constants as sc

def tlsAndMBT(params, temps, data, eps = None):
    """Return residual of model, weighted by uncertainties.

    Return value:
    residual -- the weighted or unweighted vector of residuals

    Arguments:
    params -- an lmfit Parameters object containing df, Fd, fRef, alpha, delta0
    temps -- a list/vector of temperatures at which to evaluate the model
    data -- a list/vector of data to compare with model
    eps -- a list/vector of uncertainty values for data

    len(temps) == len(data) == len(eps)"""
    #Unpack parameter values from params
    Fd = params['Fd'].value
    f0 = params['f0'].value
    alpha = params['alpha'].value
    delta0 = params['delta0'].value

    #Calculate model from parameters
    model = f0+f0*(Fd/sc.pi* #TLS contribution
             (np.real(digamma(0.5+sc.h*f0/(1j*2*sc.pi*sc.k*(temps))))
              -np.log(sc.h*f0/(2*sc.pi*sc.k*(temps))))-

             alpha/4.0* #MBD contribution
             (np.sqrt((2*sc.pi*sc.k*temps)/delta0)*
              np.exp(-delta0/(sc.k*temps))+
              2*np.exp(-delta0/(sc.k*temps))*
              np.exp(-sc.h*f0/(2*sc.k*temps))*
              np.i0(sc.h*f0/(2*sc.k*temps))))


    #Weight the residual if eps is supplied
    if data is not None:
        if eps is not None:
            residual = (model-data)/eps
        else:
            residual = (model-data)

        return residual
    else:
        return model

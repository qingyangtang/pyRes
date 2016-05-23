import pandas as pd
import numpy as np

#This is a glorified dictionary with a custom initalize method. It takes a list
#of resonator objects that have been fit, and then sets up a
#dict of pandas DataFrame objects, one for each interesting fit parameter
#This adds no new information, but makes accessing the fit data easier
class ResonatorSweep(dict):
    """Dictionary object with custom __init__ method"""


    def __init__(self, resList):
        """Formats various scalar quantities into easily parsed pandas DataFrame objects.

        Arguments:
        self -- reference to self, required for all Class methods
        resList -- a list of Resonator objects

        Created quantities:
        self.tvec -- index of temperature values
        self.pvec -- index of power values

        Note: Temperature data is binned into 5 mK spaced bins for compactness.
        Actual temperature value is stored in the 'temps' field."""

        #Start with the list of fit parameters, want to save all of them
        #Can just use the first resonator's list, as they are all the same.
        #params is NOT an lmfit object.
        params = resList[0].params.keys()

        #Add a few more
        params.append('temps') #Actual temperature value of measured resonator
        params.append('fmin') #Frequency at magnitude minimum
        params.append('chisq') #Chi-squared value from fit
        params.append('redchi') #Reduced chi-squared value
        params.append('feval') #Number of function evaluations to converge on fit

        #Loop through the resList and make lists of power and index temperature
        tvals = np.empty(len(resList))
        pvals = np.empty(len(resList))

        for index, res in enumerate(resList):
            tvals[index] = res.itemp #use itemp to minimize empty data fields
            pvals[index] = res.pwr

        #Create index vectors containing only the unique values from each list
        self.tvec = np.unique(tvals)
        self.pvec = np.unique(pvals)

        #Loop through the parameters list and create a DataFrame for each one
        for pname in params:
            #Start out with a 2D dataframe full of NaN of type float
            #Row and Column indices are temperature and power values
            self[pname] = pd.DataFrame(np.nan, index = self.tvec, columns = self.pvec)

            #Fill it with as much data as exists
            for res in resList:
                if pname in res.S21result.params.keys():
                    self[pname][res.pwr][res.itemp] = res.S21result.params[pname].value
                elif pname == 'temps':
                    #Since we bin the temps by 0.005 mK for indexing, store the actual temp here
                    self[pname][res.pwr][res.itemp] = res.temp
                elif pname == 'fmin':
                    self[pname][res.pwr][res.itemp] = res.fmin
                elif pname == 'chisq':
                    self[pname][res.pwr][res.itemp] = res.S21result.chisqr
                elif pname == 'redchi':
                    self[pname][res.pwr][res.itemp] = res.S21result.redchi
                elif pname == 'feval':
                    self[pname][res.pwr][res.itemp] = res.S21result.nfev

#Index a list of resonator objects easily
def indexResList(resList, temp, pwr, itemp=True):
    """Index resList by temp and pwr.

    Returns:
    index -- an int corresponding to the location of the Resonator specified by the Arguments

    Arguments:
    resList -- a list of Resonator objects
    temp -- the temperature of a single Resonator object
    pwr -- the power of a single Resonator object
    itemp -- boolean switch to determine whether lookup uses temp or itemp (rounded value of temp)

    Note:
    The combination of temp and pwr must be unique. indexResList does not check for duplicates."""
    for index, res in enumerate(resList):
        if itemp is True:
            if res.itemp == temp and res.pwr == pwr:
                return index
        else:
            if res.temp == temp and res.pwr == pwr:
                return index

    return None
""" 
This module provides compute functions and classes for edge_profiles ids data

`more about edge_profiles ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/edge_profiles.html>`_.

"""

import functools
import itertools
import logging
from typing import Union
import numpy as np

import database_tools.init_mendeleiev as mend
import unicodedata
logger = logging.getLogger("module")


class DistributionSourcesCompute:
    def __init__(self, ids):
        self.ids = ids
    
    def getRhoTorNorm(self)->Union[None,np.ndarray]:
        """
        The function `getRhoTorNorm` returns the normalized toroidal rho values from a given time slice
        of a source.
        
        Args:
            timeSlice (int): The parameter "timeSlice" is an integer that represents the time slice for which you want to retrieve the value of "rho_tor_norm". 
        
        Returns:
            the variable `rho_tor_norm`.
        """
        rho_tor_norm = None
        try:
            rho_tor_norm = self.ids.source[0].profiles_1d[0].grid.rho_tor_norm
            if len(rho_tor_norm) == 0 and len(self.ids.source[0].profiles_1d[0].grid.rho_tor)>0:
                nrho = len(self.ids.source[0].profiles_1d[0].grid.rho_tor)
                rho_tor_norm = self.ids.source[0].profiles_1d[0].grid.rho_tor/self.ids.source[0].profiles_1d[0].grid.rho_tor[nrho-1]
        except Exception:
            logger.critical("distribution_sources.source[0].profiles_1d[0].grid.rho_tor(_norm) could not be read")
        return rho_tor_norm
    
    def getVolume(self)->Union[None,np.ndarray]:
        """
        The function `getVolume` retrieves the volume from a specific time slice of a source's profiles.
        
        Args:
            timeSlice (int): The parameter "timeSlice" is an optional integer that specifies the index of the time slice for which you want to retrieve the volume. 
        
        Returns:
            the volume of a grid at a given time slice. The volume is obtained from the `distribution_sources.source[timeSlice].profiles_1d[0].grid.volume` attribute. If the volume cannot be read, the function returns `None`.
        """
        volume = None
        try:
            volume = self.ids.source[0].profiles_1d[0].grid.volume
        except Exception:
            logger.critical("distribution_sources.source[0].profiles_1d[0].grid.volume could not be read")
        return volume

    
    def getSourceInfo(self):
        nrho = len(self.getRhoTorNorm())
        sourcesDict={}
        counter = 0
        for source in self.ids.source:
            mlabel1 = unicodedata.normalize('NFKD', source.process[0].type.description).encode('ascii','ignore')
            mlabel2 = unicodedata.normalize('NFKD', source.process[0].reactant_energy.description).encode('ascii','ignore')
            particles = source.profiles_1d[0].particles
            if len(source.profiles_1d[0].particles) < 1:
                logger.warning('distribution_sources.source[isource].profiles_1d[0].particles could not be read')
                particles = np.asarray([np.nan]*nrho)
        
            sourceInfo = {
                "label": (mlabel1 + b'; ' + mlabel2).decode(),
                "particles": particles,
                "powerInKW": source.global_quantities[0].power * 1.0e-3,
            }
            sourcesDict[counter] = sourceInfo
            counter=counter+1
        return sourcesDict

    
        
# Read quantities for this time slice
# ds_slice = input.get_slice("distribution_sources",time,1)
# nsources = len(ds_slice.source)
# if nsources>1:
#     print('Distribution_sources contains '+str(nsources)+' sources', file=sys.stderr)
# else:
#     print('Distribution_sources contains '+str(nsources)+' source', file=sys.stderr)



# if sum(active)==0:
#     print('No active neutron sources --> Leave.', file=sys.stderr)
#     exit()

# # ----------------------------------------------------------------------

# # Rho profile (mandatory)
# nrho=0
# try:
#     rho_tor_norm = distribution_sources.source[0].profiles_1d[0].grid.rho_tor_norm
#     nrho = len(rho_tor_norm)
#     if nrho == 0:
#         if len(distribution_sources.source[0].profiles_1d[0].grid.rho_tor)>0:
#             nrho = len(distribution_sources.source[0].profiles_1d[0].grid.rho_tor)
#             rho_tor_norm = distribution_sources.source[0].profiles_1d[0].grid.rho_tor/distribution_sources.source[0].profiles_1d[0].grid.rho_tor[nrho-1]
# except:
#     print('distribution_sources.source[0].profiles_1d[0].grid.rho_tor(_norm) could not be read', file=sys.stderr)
#     print('----> Aborted.', file=sys.stderr)
#     exit()
# if nrho==0:
#     print('core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty', file=sys.stderr)
#     print('----> Aborted.', file=sys.stderr)
#     exit()

# if nrho==0:
#     print('distribution_sources.source[0].profiles_1d[0].grid.rho_tor_norm) is empty', file=sys.stderr)
#     print('----> Aborted.', file=sys.stderr)
#     exit()


# # Number of distribution sources
# nsources = len(distribution_sources.source)

# # Toroidal velocity profile
# for isource in range(nsources):
#     if len(distribution_sources.source[isource].profiles_1d[0].particles) < 1:
#         print('distribution_sources.source[isource].profiles_1d[0].particles could not be read', file=sys.stderr)
#         distribution_sources.source[isource].profiles_1d[0].particles = asarray([nan]*nrho)

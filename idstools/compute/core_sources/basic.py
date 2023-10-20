""" 
This module provides compute functions and classes for core_sources ids data

`more about core_profiles ids https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_sources.html_.

"""
import logging
import numpy as np

logger = logging.getLogger("module")


class CoreSourcesCompute:
    def __init__(self, ids):
        self.ids = ids

    def getSources(self):
        """
        The `getSources` function retrieves information about sources, including their name, particle flux, energy flux, and ion properties, and returns a dictionary containing this information.

        Returns:
            The function `getSources` returns a dictionary containing information about the sources. The dictionary has the following structure:
            {0: {'energy_flux': 22081836.173650958,
                'ions': {0: 
                            {'a': 2.0,
                            'energy_flux': None,
                            'particles_flux': 4.947616643196025e+21,
                            'z_ion': -9e+40,
                            'z_n': 1.0
                            },
                        'name': 'total',
                        'particles_flux': None
                        },
                }
            }
        """
        sourcesDict = {}
        for sourceIndex, source in enumerate(self.ids.source):
            sourceDict = {
                "name": source.identifier.name,
            }
            if len(source.profiles_1d[0].electrons.particles) != 0:
                sourceDict["particles_flux"] = np.trapz(
                    source.profiles_1d[0].electrons.particles,
                    source.profiles_1d[0].grid.volume,
                )
            else:
                sourceDict["particles_flux"] = None
            if len(source.profiles_1d[0].electrons.energy) != 0:
                sourceDict["energy_flux"] = np.trapz(
                    source.profiles_1d[0].electrons.energy,
                    source.profiles_1d[0].grid.volume,
                )
            else:
                sourceDict["energy_flux"] = None
            ionsDict = {}
            for ionIndex, ion in enumerate(source.profiles_1d[0].ion):
                ionDict = {
                    "a": ion.element[0].a,
                    "z_n": ion.element[0].z_n,
                    "z_ion": ion.z_ion,
                }
                if len(ion.particles) != 0:
                    ionDict["particles_flux"] = np.trapz(
                        ion.particles, source.profiles_1d[0].grid.volume
                    )
                else:
                    ionDict["particles_flux"] = None
                if len(ion.energy) != 0:
                    ionDict["energy_flux"] = np.trapz(
                        ion.energy, source.profiles_1d[0].grid.volume
                    )
                else:
                    ionDict["energy_flux"] = None
                ionsDict[ionIndex] = ionDict
            sourceDict["ions"] = ionsDict
            sourcesDict[sourceIndex] = sourceDict
        return sourcesDict

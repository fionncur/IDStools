""" 
This module provides compute functions and classes for core_transport ids data

`more about core_profiles ids https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_transport.html_.

"""
import logging
import numpy as np

logger = logging.getLogger("module")


class CoreTransportCompute:
    def __init__(self, ids):
        self.ids = ids

    def getFluxes(self):
        """
        The function `getFluxes` returns a dictionary containing information about fluxes in a model,
        including particle and energy fluxes for electrons and ions.

        Returns:
            a dictionary called `fluxesDict`. Following is the structure
            {0:
                {
                    'energy_flux': None,
                    'flux_multiplier': -9e+40,
                    'ions':
                        {0:
                            {'a': 2.0,
                            'energy_flux': None,
                            'particles_flux': None,
                            'z_ion': -9e+40,
                            'z_n': 1.0
                            },
                        },
                        'name': 'combined',
                        'particles_flux': None
                },
            }
        """
        fluxesDict = {}
        for modelIndex, model in enumerate(self.ids.model):
            fluxDict = {
                "name": model.identifier.name,
                "flux_multiplier": model.flux_multiplier,
            }
            if len(model.profiles_1d[0].electrons.particles.flux) != 0:
                gridFluxSurface = (
                    np.asarray(
                        [np.nan] * len(model.profiles_1d[0].electrons.particles.flux)
                    )
                    if len(model.profiles_1d[0].grid_flux.surface) == 0
                    else model.profiles_1d[0].grid_flux.surface
                )

                fluxDict["particles_flux"] = (
                    model.profiles_1d[0].electrons.particles.flux * gridFluxSurface
                )[-1]
            else:
                fluxDict["particles_flux"] = None
            if len(model.profiles_1d[0].electrons.energy.flux) != 0:
                gridFluxSurface = (
                    np.asarray(
                        [np.nan] * len(model.profiles_1d[0].electrons.energy.flux)
                    )
                    if len(model.profiles_1d[0].grid_flux.surface) == 0
                    else model.profiles_1d[0].grid_flux.surface
                )

                fluxDict["energy_flux"] = (
                    model.profiles_1d[0].electrons.energy.flux * gridFluxSurface
                )[-1]
            else:
                fluxDict["energy_flux"] = None
            ionsDict = {}
            for ionIndex, ion in enumerate(model.profiles_1d[0].ion):
                ionDict = {
                    "a": ion.element[0].a,
                    "z_n": ion.element[0].z_n,
                    "z_ion": ion.z_ion,
                }
                if len(ion.particles.flux) != 0:
                    ionDict["particles_flux"] = (
                        ion.particles.flux * model.profiles_1d[0].grid_flux.surface[-1]
                    )
                else:
                    ionDict["particles_flux"] = None
                if len(ion.energy.flux) != 0:
                    ionDict["energy_flux"] = (
                        ion.energy.flux * model.profiles_1d[0].grid_flux.surface[-1]
                    )
                else:
                    ionDict["energy_flux"] = None
                ionsDict[ionIndex] = ionDict
            fluxDict["ions"] = ionsDict
            fluxesDict[modelIndex] = fluxDict
        return fluxesDict

""" 
This module provides compute functions and classes for core_transport ids data

`more about core_profiles ids https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_transport.html_.

"""
import logging

logger = logging.getLogger("module")


class CoreTransportCompute:
    def __init__(self, ids):
        self.ids = ids

    def getFluxes(self):
        fluxesDict = {}
        for modelIndex, model in enumerate(self.ids.model):
            fluxDict = {
                "name": model.identifier.name,
                "flux_multiplier": model.flux_multiplier,
            }
            if len(model.profiles_1d[0].electrons.particles.flux) != 0:
                fluxDict["particles_flux"] = (
                    model.flux_multiplier(
                        (
                            model.profiles_1d[0].electrons.particles.flux
                            * model.profiles_1d[0].grid_flux.surface
                        )[-1]
                    ),
                )
            else:
                fluxDict["particles_flux"] = None
            if len(model.profiles_1d[0].electrons.energy.flux) != 0:
                fluxDict["energy_flux"] = (
                    model.profiles_1d[0].electrons.energy.flux
                    * model.profiles_1d[0].grid_flux.surface
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

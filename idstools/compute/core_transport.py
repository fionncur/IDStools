"""
This module provides compute functions and classes for core_transport ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import numpy as np

logger = logging.getLogger("module")


class CoreTransportCompute:
    def __init__(self, ids):
        self.ids = ids

    def get_fluxes(self, time_slice):
        """
        The function `get_fluxes` returns a dictionary containing information about fluxes in a model,
        including particle and energy fluxes for electrons and ions.

        Returns:
            a dictionary called `fluxes_dict`. Following is the structure

            .. code-block:: python

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
        fluxes_dict = {}

        for model_index, model in enumerate(self.ids.model):
            flux_dict = {
                "name": ("Not defined" if model.identifier.name == "" else model.identifier.name),
                "flux_multiplier": model.flux_multiplier,
            }
            if len(model.profiles_1d[time_slice].electrons.particles.flux) != 0:
                grid_flux_surface = (
                    np.asarray([np.nan] * len(model.profiles_1d[time_slice].electrons.particles.flux))
                    if len(model.profiles_1d[time_slice].grid_flux.surface) == 0
                    else model.profiles_1d[time_slice].grid_flux.surface
                )
                flux_dict["particles_flux"] = (
                    model.profiles_1d[time_slice].electrons.particles.flux * grid_flux_surface
                )[-1]
            else:
                flux_dict["particles_flux"] = None
            if len(model.profiles_1d[time_slice].electrons.energy.flux) != 0:
                grid_flux_surface = (
                    np.asarray([np.nan] * len(model.profiles_1d[time_slice].electrons.energy.flux))
                    if len(model.profiles_1d[time_slice].grid_flux.surface) == 0
                    else model.profiles_1d[time_slice].grid_flux.surface
                )

                flux_dict["energy_flux"] = (model.profiles_1d[time_slice].electrons.energy.flux * grid_flux_surface)[-1]
            else:
                flux_dict["energy_flux"] = None
            ions_dict = {}
            grid_flux_surface = (
                np.nan
                if len(model.profiles_1d[time_slice].grid_flux.surface) == 0
                else model.profiles_1d[time_slice].grid_flux.surface
            )
            for ion_index, ion in enumerate(model.profiles_1d[time_slice].ion):
                ion_name = "--"
                if "label" in dir(ion):
                    if ion.label.has_value:
                        ion_name = ion.label.value
                elif "name" in dir(ion):
                    if ion.name.has_value:
                        ion_name = ion.name.value
                # print(ion.name)
                ion_dict = {
                    "name": ion_name,
                    "a": ion.element[0].a if ion.element[0].a else "--",
                    "z_n": ion.element[0].z_n if ion.element[0].z_n else "--",
                    "z_ion": ion.z_ion if ion.z_ion.has_value else "--",
                }
                if len(ion.particles.flux) != 0:
                    ion_dict["particles_flux"] = (ion.particles.flux * grid_flux_surface)[-1]
                else:
                    ion_dict["particles_flux"] = None
                if len(ion.energy.flux) != 0:
                    ion_dict["energy_flux"] = (ion.energy.flux * grid_flux_surface)[-1]
                else:
                    ion_dict["energy_flux"] = None
                ions_dict[ion_index] = ion_dict
            flux_dict["ions"] = ions_dict
            fluxes_dict[model_index] = flux_dict
        return fluxes_dict

import logging
import numpy as np
from ..compute.core_transport import CoreTransportCompute

logger = logging.getLogger(f"module.{__name__}")


class CoreTransportView:
    def __init__(self, ids):
        self.coreTransportCompute = CoreTransportCompute(ids)
        self.ids = ids

    def viewFluxes(self):
        """
        The `viewFluxes` function prints out flux information for electrons and ions.
        """
        fluxesDict = self.coreTransportCompute.getFluxes()

        for _, fluxDict in fluxesDict.items():
            print(f'{fluxDict["name"]} ({fluxDict["flux_multiplier"]})')
            print(f"{'electrons': >30}", end="")
            # electrons
            if fluxDict["particles_flux"] is None:
                print(f"{'particles(--)' : >25}", end="")
            else:
                print("     particles %13.6e" % (fluxDict["particles_flux"]), end="")
            if fluxDict["energy_flux"] is None:
                print(f"{'energy(--)' : >25}")
            else:
                print("     energy %13.6e" % ((fluxDict["energy_flux"])))
            # ions
            print(
                f"{'a' : >10}{'z_n' : >10}{'z_ion' : >10}{'particles' : >25}{'energy' : >25}"
            ),

            for _, ionDict in fluxDict["ions"].items():
                print(
                    f"{ionDict['a'] : >10}{ionDict['z_n'] : >10}{ionDict['z_ion'] : >10}",
                    end="",
                )
                if ionDict["particles_flux"] is None or all(
                    np.isnan(ionDict["particles_flux"])
                ):
                    print(f"{'--' : >25}", end="")
                else:
                    print(f"{ionDict['particles_flux'] : >25.6e}", end="")
                if ionDict["energy_flux"] is None or all(
                    np.isnan(ionDict["energy_flux"])
                ):
                    print(f"{'--' : >25}")
                else:
                    print(f"{ionDict['energy_flux'] : >25.6e}")

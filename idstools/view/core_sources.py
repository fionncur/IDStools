import logging

from idstools.compute.core_sources import CoreSourcesCompute

logger = logging.getLogger(f"module.{__name__}")


class CoreSourcesView:
    def __init__(self, ids):
        self.coreSourcesCompute = CoreSourcesCompute(ids)
        self.ids = ids

    def viewSources(self):
        """
        The `viewSources` function prints information about sources, including their name, electron
        flux, energy flux, and ion flux.
        """
        sourcesDict = self.coreSourcesCompute.getSources()

        for _, sourceDict in sourcesDict.items():
            print(f'{sourceDict["name"]}')
            print(f"{'electrons': >30}", end="")
            # electrons
            if sourceDict["particles_flux"] is None:
                print(f"{'particles(--)' : >25}", end="")
            else:
                print("     particles %13.6e" % (sourceDict["particles_flux"]), end="")
            if sourceDict["energy_flux"] is None:
                print(f"{'energy(--)' : >25}")
            else:
                print("     energy %13.6e" % ((sourceDict["energy_flux"])))
            # ions
            print(
                f"{'a' : >10}{'z_n' : >10}{'z_ion' : >10}{'particles' : >25}{'energy' : >25}"
            ),

            for _, ionDict in sourceDict["ions"].items():
                print(
                    f"{ionDict['a'] : >10}{ionDict['z_n'] : >10}{ionDict['z_ion'] : >10}",
                    end="",
                )
                if ionDict["particles_flux"] is None:
                    print(f"{'--' : >25}", end="")
                else:
                    print(f"{ionDict['particles_flux'] : >25.6e}", end="")
                if ionDict["energy_flux"] is None:
                    print(f"{'--' : >25}")
                else:
                    print(f"{ionDict['energy_flux'] : >25.6e}")

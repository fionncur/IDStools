#!/usr/bin/env python3
# $ ids_compo -s 131047 -r 4
# !   No edge_profiles IDS in the data-entry.
# core +  edge  -
#    ------------
# core_profiles
#    ------------
#    species:      H         D         T         He3       He4       Be        Ne
#    a:            1.0       2.0       3.0       3.0       4.0       9.0       20.0
#    z:            1.0       1.0       1.0       2.0       2.0       4.0       10.0
#    n_over_ntot:  5.29e-06  0.460     0.493     7.01e-07  0.011     0.024     0.012
#    n_over_ne:    4.45e-06  0.387     0.414     5.89e-07  9.58e-03  0.020     0.010
#    n_over_n_maj: 1.07e-05  0.933     1.000     1.42e-06  0.023     0.048     0.024

from idstools.cli import *
import argparse
import imas
import logging
import numpy as np
import os
import sys

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from idstools2.view.core_profiles.basic import CoreProfilesView
from idstools2.view.edge_profiles.basic import EdgeProfilesView

parser = argparse.ArgumentParser(
    description="---- Display the plasma composition from the core_profiles IDS",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
parser.add_argument("-i", "--info", action="store_true", help="Show information")
parser.add_argument("--debug", action="store_true", help="Show debugging")

args = parser.parse_args()


def setup_logger(logger_name, isdebug, isinfo):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.WARN)  # default
    if isdebug:
        logger.setLevel(logging.DEBUG)
    if isinfo:
        logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    if isdebug:
        ch.setLevel(logging.DEBUG)
    if isinfo:
        ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = setup_logger("module", args.debug, args.info)

logger.info("----------------------------------------------------------------")
logger.info(
    """
    a       = Mass of atom [Atomic Mass Unit]
    z       = Nuclear charge [Elementary Charge Unit]
    ne      = sum(volume * electron_density)
    volume  = sum(volume of each cell)
    nspec_over_ntot : Species density list / Sum of Species Density (ntot)
    nspec_over_ne   : Species density list / Total no. electrons (ne)
    nspec_over_nmaj : Species density list / Species density[Index of Maximum Density Species]"""
)
logger.info("----------------------------------------------------------------")
connection = imas.DBEntry(
    get_backend_id(args.backend),
    args.database,
    args.shot,
    args.run,
    user_name=args.user,
    data_version=args.version,
)
err, _ = connection.open()
if err != 0:
    logger.critical(
        f"Shot {args.shot}, run {args.run} for user {args.user} and database {args.database} is not reachable ----> abort!",
        file=sys.stderr,
    )
    sys.exit(err)

# Prepare IDS with highest density data from core profiles
core_profiles_ids = imas.core_profiles()
try:
    core_profiles_ids.time = connection.partial_get("core_profiles", "time")
except:
    core_profiles_ids.time = None

edge_profiles_ids = imas.edge_profiles()
try:
    edge_profiles_ids.time = connection.partial_get("edge_profiles", "time")
except:
    edge_profiles_ids.time = None

core_profile_exists = True
edge_profile_exists = True
if core_profiles_ids.time is None:
    core_profile_exists = False
if edge_profiles_ids.time is None:
    edge_profile_exists = False
slice_index = 0
if core_profiles_ids.time is not None:
    ne0_list = connection.partial_get(
        "core_profiles", "profiles_1d(:)/electrons/density(0)"
    )
    slice_index = np.argmax(ne0_list)
    profiles_1d_slice = connection.partial_get(
        "core_profiles", f"profiles_1d({slice_index})"
    )
    logger.info(
        "core_profiles IDS:Using time slice where maximum electrons density is present, Time slice:"
        + str(slice_index)
    )
    core_profiles_ids.profiles_1d.resize(1)
    core_profiles_ids.profiles_1d[0] = profiles_1d_slice

    returnstatus = CoreProfilesView.view_plasma_composition_with_species_concentration(
        core_profiles_ids, 0
    )
    if returnstatus == 0:
        core_profile_exists = False
        logger.critical(
            "core_profiles IDS: IDS exists but time slice doesn't exists. --> Abort."
        )
    elif returnstatus == -1:
        core_profile_exists = False
        logger.critical("core_profiles IDS:IDS exists but volume is not set")
        logger.warning("core_profiles IDS :Retrieving volume from equilibrium IDS")
        equilibrium = imas.equilibrium()
        equilibrium.time_slice.resize(1)
        volume = connection.partial_get(
            "equilibrium", f"time_slice({slice_index})/profiles_1d/volume"
        )
        returnstatus = (
            CoreProfilesView.view_plasma_composition_with_species_concentration(
                core_profiles_ids, 0, volume=volume
            )
        )
        core_profile_exists = True

else:
    logger.critical(
        "core_profiles IDS:No core_profiles IDS in the data-entry --> Abort."
    )


# # TODO There is no relation of Slice index calculated above so getting data of 0th slice. and Why only 0th slice

if edge_profiles_ids.time is not None:
    logger.info(
        "edge_profiles IDS:Using time slice where maximum electrons density is present in core, Time slice:"
        + str(slice_index)
    )
    edge_profiles_ids.ggd.resize(1)
    edge_profiles_ids.ggd[0] = connection.partial_get(
        "edge_profiles", f"ggd({slice_index})"
    )

    edge_profiles_ids.grid_ggd.resize(1)
    edge_profiles_ids.grid_ggd[0] = connection.partial_get(
        "edge_profiles", f"grid_ggd({slice_index})"
    )

    returnstatus = EdgeProfilesView.view_plasma_composition_with_species_concentration(
        edge_profiles_ids, 0
    )
    if returnstatus == 0:
        edge_profile_exists = False
        logger.critical(
            "edge_profiles IDS:IDS exists but time slice doesn't exists. --> Abort."
        )
    elif returnstatus == -1:
        logger.warning(
            "edge_profiles IDS:IDS exists but volume is not set. --> Trying nearby time slice. This may take a while.."
        )
        edge_profiles = connection.get("edge_profiles")
        time_slices_count = len(edge_profiles.grid_ggd)
        index_list = []
        for counter in range(1, 10):
            if slice_index - counter >= 0 and slice_index - counter < time_slices_count:
                index_list.append(slice_index - counter)
            if slice_index + counter >= 0 and slice_index + counter < time_slices_count:
                index_list.append(slice_index + counter)
        for time_slice in index_list:
            index = 4
            elements = edge_profiles.grid_ggd[time_slice].grid_subset[index].element
            grid_subset_name = (
                edge_profiles.grid_ggd[time_slice].grid_subset[index].identifier.name
            )
            # check if grid_subset[4] identifier name is cells, if not, find out 'cells' index
            index_counter = 0
            if grid_subset_name.lower() != "cells":
                for subset in edge_profiles.grid_ggd[time_slice].grid_subset:
                    if subset.identifier.name.lower() == "cells":
                        elements = (
                            edge_profiles.grid_ggd[time_slice]
                            .grid_subset[index_counter]
                            .element
                        )
                        grid_subset_name = (
                            edge_profiles.grid_ggd[time_slice]
                            .grid_subset[index_counter]
                            .identifier.name
                        )
                        index = index_counter
                        break
                    index_counter = index_counter + 1
            if len(elements) != 0:
                logger.info(
                    "edge_profiles IDS:Using nearby time slice in edge where maximum electrons density is present in core, Time slice:"
                    + str(time_slice)
                )
                edge_profiles_ids.ggd.resize(1)
                edge_profiles_ids.ggd[0] = connection.partial_get(
                    "edge_profiles", f"ggd({time_slice})"
                )

                edge_profiles_ids.grid_ggd.resize(1)
                edge_profiles_ids.grid_ggd[0] = connection.partial_get(
                    "edge_profiles", f"grid_ggd({time_slice})"
                )

                returnstatus = (
                    EdgeProfilesView.view_plasma_composition_with_species_concentration(
                        edge_profiles_ids, 0
                    )
                )
                if returnstatus == 0:
                    edge_profile_exists = False
                    logger.critical(
                        "edge_profiles IDS:IDS exists but time slice doesn't exists. --> Abort."
                    )
                elif returnstatus == -1:
                    edge_profile_exists = False
                    logger.warning(
                        "edge_profiles IDS:IDS exists but volume is not set."
                    )
                break
else:
    logger.critical(
        "edge_profiles IDS:No edge_profiles IDS in the data-entry. --> Abort."
    )

profile_availability_string = ""
if core_profile_exists is False:
    profile_availability_string += "core -\t"
else:
    profile_availability_string += "core +\t"

if edge_profile_exists is False:
    profile_availability_string += "edge -\t"
else:
    profile_availability_string += "edge +\t"

print(profile_availability_string)

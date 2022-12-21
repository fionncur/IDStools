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
import numpy as np
import os
import sys

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from src.view.core_profiles.functions import CoreProfilesView
from src.view.edge_profiles.functions import EdgeProfilesView

parser = argparse.ArgumentParser(
    description="---- Display the plasma composition from the core_profiles IDS",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)

args = parser.parse_args()

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
    print(
        f"!   Shot {args.shot}, run {args.run} for user {args.user} and database {args.database} is not reachable ----> abort!",
        file=sys.stderr,
    )
    sys.exit(err)

# Prepare IDS with highest density data from core profiles
core_profiles_ids = imas.core_profiles()
core_profiles_ids.time = connection.partial_get("core_profiles", "time")
ne0_list = connection.partial_get(
    "core_profiles", "profiles_1d(:)/electrons/density(0)"
)
slice_index = np.argmax(ne0_list)

profiles_1d_slice = connection.partial_get(
    "core_profiles", f"profiles_1d({slice_index})"
)
core_profiles_ids.profiles_1d.resize(1)
core_profiles_ids.profiles_1d[0] = profiles_1d_slice

CoreProfilesView.view_plasma_composition_with_species_concentration(
    core_profiles_ids, 0
)

# 123260 1
# edge_profiles_ids = imas.edge_profiles()
# edge_profiles_ids.time = connection.partial_get("edge_profiles", "time")
# # TODO There is no relation of Slice index calculated above so getting data of 0th slice. and Why only 0th slice
# edge_profiles_ids.ggd.resize(1)
# edge_profiles_ids.ggd[0] = connection.partial_get("edge_profiles", f"ggd({0})")

# edge_profiles_ids.grid_ggd.resize(1)
# edge_profiles_ids.grid_ggd[0] = connection.partial_get(
#     "edge_profiles", f"grid_ggd({0})"
# )

# EdgeProfilesView.view_plasma_composition_with_species_concentration(
#     edge_profiles_ids, 0
)

import argparse
import imas
import numpy as np
import os
import sys

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from idstools.cli import get_backend_id
from idstools.cli import imas_parser

from idstools2.compute.core_profiles.basic import CoreProfilesCompute
from idstools2.compute.equilibrium.basic import EquilibriumCompute

from idstools2.database.basic import read_ids

from idstools2.view.common.basic import Canvas
from idstools2.view.core_profiles.basic import CoreProfilesView
from idstools2.view.domain.ecstray.basic import EcStrayView
from idstools2.view.equilibrium.basic import EquilibriumView
from idstools2.view.tbd.basic import TbdView
from idstools2.view.waves.basic import WavesView

from idstools2.input_processing.basic import (
    beam_wall_crossing,
    check_rays_into_divertor,
    read_launching_parameters,
    read_torbeam_output,
    read_wall,
)

parser = argparse.ArgumentParser(
    description="---- Display the plasma equilibrium from the equilibrium IDS",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
parser.add_argument(
    "-t", "--time", help="Time (default=middle)", type=float, default=-99.0
)
parser.add_argument(
    "-o",
    "--occurrence",
    help="Occurrence number (default=%(default)s)",
    type=int,
    default=0,
)
parser.add_argument("-p", "--plotrho", help="Plots rho(R,Z)", action="store_true")
parser.add_argument(
    "-a",
    "--allInfo",
    help="Adds all extra provenance info to the plot",
    action="store_true",
)
parser.add_argument(
    "-c",
    "--pfcoils",
    help="Show pf coils overlay on the plot",
    action="store_true",
)
args = parser.parse_args()

database_abs_path = ""
if args.user == "public":
    database_abs_path = (
        os.environ["IMAS_HOME"] + "/shared/imasdb/" + args.database + "/3"
    )
else:
    database_abs_path = (
        os.path.expanduser("~{}".format(args.user))
        + "/public/imasdb/"
        + args.database
        + "/3"
    )
hostdir = os.environ["HOSTNAME"] + ":" + database_abs_path

connection = imas.DBEntry(
    get_backend_id(args.backend), args.database, args.shot, args.run, args.user
)
err, n = connection.open()
if err != 0:
    # TODO chek if you can raise exception or just print or may be use logger
    print(
        "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
            args.shot, args.run, args.user, args.database
        ),
        file=sys.stderr,
    )
    print("----> Aborted.", file=sys.stderr)
    exit()


time_index_eq = 0
time_index_cp = 0
time_index_wv = 0

current_file_path = os.path.dirname(os.path.abspath(__file__))

scenario_file = os.path.join(current_file_path, "input/scenario.yaml")
wallfile = os.path.join(current_file_path, "input/wall2d.txt")
filelaunchers = os.path.join(current_file_path, "input/ec_waveforms.yaml")
path_result = os.path.join(current_file_path, "results/")

wall2d = read_wall(wallfile)

# # Read launching parameters from EC waveform file
launching_parameters = read_launching_parameters(filelaunchers)
# # Read beam extra variables from Torbeam output ascii files
beam_output, time_array_wv = read_torbeam_output(launching_parameters, path_result)
# # Check if rays go into the divertor
check_rays_into_divertor(wall2d, beam_output)
# # Calculates where the beams cross the wall
beam_wall = beam_wall_crossing(wall2d, launching_parameters, beam_output)

equilibrium_ids, core_profiles_ids, waves_ids = read_ids(scenario_file)


# TODO Is it wise to get common timestamp and make zero hold of other timestamps?
# Or just follow what we have here. This is ellegant in terms of performance
def iround(x, xi):
    return np.argmin(np.abs(x - xi))


eqcomputeobj = EquilibriumCompute(equilibrium_ids)
coreprofilesobj = CoreProfilesCompute(core_profiles_ids)
waveobj = EquilibriumCompute(waves_ids)

time_array_eq = eqcomputeobj.ids.time  # Plot Ip
time_array_cp = coreprofilesobj.ids_object.time
time_array_wv = waveobj.ids.time

time_slice = 5.0

# # Indices for time arrays in equilibrium, core_profiles, waves IDSs
time_index_eq = iround(time_array_eq, time_slice)
time_index_cp = iround(time_array_cp, time_slice)
time_index_wv = iround(time_array_wv, time_slice)

canvas = Canvas(3, 2)

# Subplot waveforms versus time
equillibriumview = EquilibriumView(equilibrium_ids)
coreprofilesview = CoreProfilesView(core_profiles_ids)
wavesview = WavesView(waves_ids)
ecstrayview = EcStrayView(equilibrium_ids, core_profiles_ids, waves_ids)

ax_waveform = canvas.add_axes(
    title="Waveforms", xlabel="Time [s]", row=0, col=0, colspan=1
)
equillibriumview.plot_ip(ax_waveform)  # Plot Ip
coreprofilesview.plot_ne0(ax_waveform)

ax_beam_index = canvas.add_axes(
    title="Beam_Index", xlabel="Beam index", row=0, col=1, colspan=1
)
wavesview.plot_beam_index(ax_beam_index)

ax_pol_view = canvas.add_axes(
    title="Poloidal view (R,Z)", xlabel="R [m]", ylabel="Z [m]", row=1, col=0, rowspan=1
)
equillibriumview.plot_poloidal_equilibrium(ax_pol_view, time_index_eq)

beam_index = 0
wavesview.plot_poloidal_traces(ax_pol_view, time_index_wv, beam_index, verbose=True)

ecstrayview.plot_resonance_layer(
    ax_pol_view, time_index_wv, time_index_eq, verbose=True
)

ecstrayview.plot_cutoff_layer(ax_pol_view, time_index_wv, time_index_cp, time_index_eq)

ax_top_view = canvas.add_axes(
    title="Top View (X,Y)", xlabel="X [m]", ylabel="Y [m]", row=1, col=1, rowspan=1
)

ax_topview_plot_eq = equillibriumview.plot_topview_equilibrium(
    ax_top_view, time_index_eq
)

ax_topview_plot_traces = wavesview.plot_topview_traces(
    ax_top_view, time_index_wv, beam_index
)

# Subplot profiles
ax_density = canvas.add_axes(
    xlabel=r"Normalised $\rho_{tor}$ [-]",
    ylabel="Density [m-3]",
    row=2,
    col=0,
    rowspan=1,
)
ax_density_plot_dens, nmax = coreprofilesview.plot_density_profile(
    ax_density, time_index_cp
)

tbdView = TbdView()
# Subplot polygon graph for beam footprints
ax_polygon = canvas.add_axes(
    title="Beam footprints on the wall",
    xlabel=r"$\phi \times R_{max}$ [Rad.m]",
    ylabel="Length along polygon [m]",
    row=2,
    col=1,
    rowspan=1,
)
# Subplot polygon graph for beam footprints
ax_polygon_plot_pol = tbdView.plot_polygon(
    ax_polygon, wall2d, beam_wall, beam_index, time_index_wv, time_index_wv
)
canvas.show()
print("done")

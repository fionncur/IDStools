#!/usr/bin/env python3

# TODO Edgeplot is added in develop2.0 developed by Anna https://confluence.iter.org/display/IMP/How+to+plot+data+from+edge_profiles
# TODO Refactor code
import argparse
import contextlib
import imas
import logging
import numpy as np
import matplotlib, os

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from idstools.cli import get_backend_id
from idstools.cli import imas_parser
from cli_helper import setup_logger

parser = argparse.ArgumentParser(
    description="---- Edge Profile plot",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)

args = parser.parse_args()

logger = setup_logger("module", logging.DEBUG)

connection = imas.DBEntry(
    get_backend_id(args.backend), args.database, args.shot, args.run, args.user
)
err, n = connection.open()
if err != 0:
    logger.error(
        f"Shot {args.shot}, run {args.run} for user={args.user} and database={args.database} does not exists"
    )
    raise Exception(
        f"Shot {args.shot}, run {args.run} for user={args.user} and database={args.database} does not exists"
    )

plot_time = 3  # s

edgeProfileIds = None
wallIds = None

try:
    edgeProfileIds = connection.get("edge_profiles")
    time_array = connection.partial_get("edge_profiles", "time")
except:
    logger.error("edge_profiles ids is not present")
    raise Exception("edge_profiles ids is not present")


try:
    # TODO Confirm about fixed wall IDS
    # wall of the tokamak
    # wall = imas.DBEntry(get_backend_id(args.backend), args.database, 121014, 11, args.user)
    # wall.open()
    # inter = wall.get("wall")
    # wall.close()
    wallIds = connection.get("wall")
except:
    logger.error("wall ids is not present")
    raise Exception("edge_profiles ids is not present")

ntime = len(time_array)

index = np.argmin(abs(plot_time - time_array))

# Read edge data from edge_profiles and interpolate on rectangular grid:
# read positions
num_vertices = len(
    edgeProfileIds.grid_ggd[index].space[0].objects_per_dimension[0].object
)
vertex_coords = np.zeros((num_vertices, 2))
for vertex_id in range(num_vertices):
    vertex_coords[vertex_id, :] = (
        edgeProfileIds.grid_ggd[index]
        .space[0]
        .objects_per_dimension[0]
        .object[vertex_id]
        .geometry[:]
    )
r_edge = vertex_coords[:, 0]
z_edge = vertex_coords[:, 1]

# interpolate on rectangular x,y grid, for example a regular grid of 400 points
num_points = 400
x, y = np.meshgrid(np.linspace(4, 8.5, num_points), np.linspace(-4.5, 4.5, num_points))

# electron density
temp = edgeProfileIds.ggd[0].electrons.density[0].values
ne_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# ion density
temp = edgeProfileIds.ggd[0].ion[0].density[0].values
ni_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# neutral density
temp = edgeProfileIds.ggd[0].neutral[0].density[0].values
n_neutral_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# can be replaced by temperature or different ion states ggd[itime].ion[i1]/state[i2]/density[0]

# find the separatrix and use it to remove the core area, otherwise the center of the 2D plot will be filled in with linearly interpolated density
index = 0
subset = 17
num_sep = len(edgeProfileIds.grid_ggd[index].grid_subset[subset].element)
sep_coords = np.zeros((num_sep, 2))
for i in range(num_sep):
    sep_coords[i, :] = (
        edgeProfileIds.grid_ggd[index]
        .space[0]
        .objects_per_dimension[0]
        .object[
            edgeProfileIds.grid_ggd[index]
            .grid_subset[subset]
            .element[i]
            .object[0]
            .index
        ]
        .geometry[:]
    )
hull = ConvexHull(sep_coords[0 : num_sep - 1, :])  # find a closed separatrix contour
separatrix = np.array([sep_coords[hull.vertices, 0], sep_coords[hull.vertices, 1]]).T
r = None
z = None
if wallIds is not None:
    with contextlib.suppress(Exception):
        r = wallIds.description_2d[0].vessel.unit[0].annular.centreline.r
        z = wallIds.description_2d[0].vessel.unit[0].annular.centreline.z
# make plots
figure = plt.figure(figsize=(10, 4))

ax0 = figure.add_subplot(1, 3, 1)
c0 = ax0.pcolor(x, y, ne_edge, vmin=0, vmax=5e19, shading="auto")
ax0.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
if r is not None and z is not None:
    ax0.plot(
        r,
        z,
        "silver",
    )
ax0.set_xlabel("R,m")
ax0.set_ylabel("Z,m")
ax0.set_title("Electron density")
figure.colorbar(c0, ax=ax0)

ax1 = figure.add_subplot(1, 3, 2)
c1 = ax1.pcolor(x, y, ni_edge, vmin=0, vmax=5e19, shading="auto")
ax1.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
if r is not None and z is not None:
    ax1.plot(
        r,
        z,
        "silver",
    )

ax1.set_xlabel("R,m")
ax1.set_ylabel("Z,m")
ax1.set_title("Ion density")
figure.colorbar(c1, ax=ax1)

ax2 = figure.add_subplot(1, 3, 3)
c2 = ax2.pcolor(x, y, n_neutral_edge, vmin=0, vmax=5e19, shading="auto")
ax2.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
if r is not None and z is not None:
    ax2.plot(
        r,
        z,
        "silver",
    )

ax2.set_xlabel("R,m")
ax2.set_ylabel("Z,m")
ax2.set_title("Neutral density")
figure.colorbar(c2, ax=ax2)

figure.tight_layout(pad=3, w_pad=5, h_pad=3)


# choose Z position for a radial profile:
Z0 = 0.0
ind = np.argmin(abs(y[:, 0] - Z0))
plt.plot(x[ind, :], ne_edge[ind, :], label="Equatorial plane")

Z0 = -4.0
ind = np.argmin(abs(y[:, 0] - Z0))
plt.plot(x[ind, :], ne_edge[ind, :], label="Divertor")
plt.title("Electron density")
plt.xlabel("R,m")
plt.ylim([0, 1.5e21])
plt.legend()
plt.show()

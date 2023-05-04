import imas
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.spatial import ConvexHull, convex_hull_plot_2d

# %matplotlib inline
# -s 134174 -r 117
# INPUT CONFIGURATION
input_user_or_path = "public"
input_database = "iter"
shot = 134174
run_in = 117
plot_time = 3  # s

try:
    input = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND, input_database, shot, run_in, input_user_or_path
    )
    input.open()
except:
    raise Exception("Could not open the IMAS file with plasma")

edge = None

try:
    edge = input.get("edge_profiles")
except:
    minor_err = 1
    print("Could not open edge_profiles")

# TIME ARRAY
try:
    time_array = input.partial_get(ids_name="equilibrium", data_path="time")
    ntime = len(time_array)
    index = np.argmin(abs(plot_time - time_array))
except:
    input.close()
    raise Exception("Could not read time values")
input.close()

# Read edge data from edge_profiles and interpolate on rectangular grid:
# read positions
num_vertices = len(edge.grid_ggd[index].space[0].objects_per_dimension[0].object)
vertex_coords = np.zeros((num_vertices, 2))
for vertex_id in range(num_vertices):
    vertex_coords[vertex_id, :] = (
        edge.grid_ggd[index]
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
temp = edge.ggd[0].electrons.density[0].values
ne_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# ion density
temp = edge.ggd[0].ion[0].density[0].values
ni_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# neutral density
temp = edge.ggd[0].neutral[0].density[0].values
n_neutral_edge = interpolate.griddata((r_edge, z_edge), temp, (x, y))
# can be replaced by temperature or different ion states ggd[itime].ion[i1]/state[i2]/density[0]

# find the separatrix and use it to remove the core area, otherwise the center of the 2D plot will be filled in with linearly interpolated density
index = 0
subset = 17
num_sep = len(edge.grid_ggd[index].grid_subset[subset].element)
sep_coords = np.zeros((num_sep, 2))
for i in range(num_sep):
    sep_coords[i, :] = (
        edge.grid_ggd[index]
        .space[0]
        .objects_per_dimension[0]
        .object[edge.grid_ggd[index].grid_subset[subset].element[i].object[0].index]
        .geometry[:]
    )
hull = ConvexHull(sep_coords[0 : num_sep - 1, :])  # find a closed separatrix contour
separatrix = np.array([sep_coords[hull.vertices, 0], sep_coords[hull.vertices, 1]]).T

# wall of the tokamak
wall = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND, "ITER_MD", 1180, 17, "public")
wall.open()
inter = wall.get_slice("wall", 0, 1)
wall.close()

# make plots
figure = plt.figure(figsize=(10, 4))

ax0 = figure.add_subplot(1, 3, 1)
c0 = ax0.pcolor(x, y, ne_edge, vmin=0, vmax=5e19, shading="auto")
ax0.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
ax0.plot(
    inter.description_2d[0].vessel.unit[0].annular.centreline.r,
    inter.description_2d[0].vessel.unit[0].annular.centreline.z,
    "silver",
)
ax0.set_xlabel("R,m")
ax0.set_ylabel("Z,m")
ax0.set_title("Electron density")
figure.colorbar(c0, ax=ax0)

ax1 = figure.add_subplot(1, 3, 2)
c1 = ax1.pcolor(x, y, ni_edge, vmin=0, vmax=5e19, shading="auto")
ax1.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
ax1.plot(
    inter.description_2d[0].vessel.unit[0].annular.centreline.r,
    inter.description_2d[0].vessel.unit[0].annular.centreline.z,
    "silver",
)
ax1.set_xlabel("R,m")
ax1.set_ylabel("Z,m")
ax1.set_title("Ion density")
figure.colorbar(c1, ax=ax1)

ax2 = figure.add_subplot(1, 3, 3)
c2 = ax2.pcolor(x, y, n_neutral_edge, vmin=0, vmax=5e19, shading="auto")
ax2.fill(separatrix[:, 0], separatrix[:, 1], facecolor="w", edgecolor="r", linewidth=3)
ax2.plot(
    inter.description_2d[0].vessel.unit[0].annular.centreline.r,
    inter.description_2d[0].vessel.unit[0].annular.centreline.z,
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

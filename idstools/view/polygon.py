import matplotlib.colorbar as cbar
import matplotlib.pyplot as plt
import numpy as np

# import matplotlib
# matplotlib.use('TKagg')
from matplotlib.colors import LogNorm

from idstools.input_processing import l2r


# TODO Wait till we have new ids and then refactor
class PolygonView:
    def __init__(self):
        pass

    def plot_polygon(self, ax, wall2d, beam_wall, ib, its, ite, init=1):
        g1e = beam_wall["g1e"]
        g2e = beam_wall["g2e"]
        re = beam_wall["re"]
        se = beam_wall["se"]
        g1l = beam_wall["g1l"]
        g2l = beam_wall["g2l"]
        rl = beam_wall["rl"]
        sl = beam_wall["sl"]
        i0 = beam_wall["I0"]
        i0e = beam_wall["I0e"]

        # now do the plotting
        # y-axis polygone segments
        edges = np.vstack([wall2d, wall2d[0, :]])
        lwall = np.zeros((len(wall2d) + 1), dtype=np.double)
        for i in range(len(lwall)):
            if i == 0:
                lwall[i] = 0.0
            else:
                lwall[i] = lwall[i - 1] + np.sqrt(
                    (edges[i, 0] - edges[i - 1, 0]) ** 2 + (edges[i, 1] - edges[i - 1, 1]) ** 2
                )
        lmin = lwall[0]
        lmax = lwall[len(lwall) - 1]
        # lmin=8
        # lmax=20
        # find coresponding polygone segments
        imin = len(np.where(lwall <= lmin)[0]) - 1
        imax = np.where(lwall >= lmax)[0][0]
        # find Rmax
        irmax = np.argmax(edges[imin : imax + 1, 0]) + imin
        # FIXME edge is not defined here, might raise runtime error
        if irmax == imin:
            rmax = edges[imin, 0] + (lmin - lwall[imin]) / (lwall[imin + 1] - lwall[imin]) * (
                edges[imin + 1, 0] - edges[imin, 0]
            )
        elif irmax == imax:
            rmax = edges[imax - 1, 0] + (lmax - lwall[imax - 1]) / (lwall[imax] - lwall[imax - 1]) * (
                edges[imax, 0] - edges[imax - 1, 0]
            )
        else:
            rmax = edges[irmax, 0]
        # if at the edge, interpolate
        y_range = np.array([lmin, lmax])
        # x-axis Torus sectors
        smin = 0.0
        smax = 18.0
        pi9 = np.double(np.pi / 9.0)
        x_range = np.array([(smin) * pi9 * rmax, smax * pi9 * rmax], dtype=np.double)
        # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
        # fig, ax = plt.subplots(figsize=(10, 5.4), constrained_layout=True)
        if init == 1:
            ax.set_xlim(left=x_range[0], right=x_range[1])
            ax.set_ylim(ymin=y_range[0], ymax=y_range[1])
        # plot boundaries of sectors
        ydata = np.linspace(y_range[0], y_range[1], num=100)
        rdata = l2r(ydata, edges, lwall)
        for i in range(18):
            x1data = pi9 * (np.double(i) + 0.5) * rmax - rdata * pi9 * 0.5
            x2data = pi9 * (np.double(i) + 0.5) * rmax + rdata * pi9 * 0.5
            if init == 1:
                ax.plot(x1data, ydata, label="S" + str(i) + "_1", color="0")
                ax.plot(x2data, ydata, label="S" + str(i) + "_2", color="0")
            else:
                ax.set_data(x1data, ydata)
                ax.set_data(x2data, ydata)
        tdata = np.linspace(0.0, 2 * np.pi, num=100, dtype=np.double)
        xydata = np.zeros((len(tdata), 2), dtype=np.double)

        # set up a color mapping
        pfmin = np.double(1e6)
        pfmax = np.double(1e9)
        nvalues = 100
        values = np.logspace(np.log10(pfmin), np.log10(pfmax), num=nvalues)
        # normieren und colormap erzeugen
        normal = LogNorm(pfmin, pfmax)
        chosen_cmap = plt.cm.inferno
        cmap = chosen_cmap(normal(values))

        # plot an entry pattern using g1e, g2e, re, se
        for i in range(len(tdata)):
            xydata[i, :] = re[ib, :] + np.cos(tdata[i]) * g1e[ib, :] + np.sin(tdata[i]) * g2e[ib, :]
        xydata[:, 0] = xydata[:, 0] + pi9 * (np.double(se[ib]) + 0.5) * rmax
        if init == 1:
            ax.plot(xydata[:, 0], xydata[:, 1], label="L" + str(ib), color="0")
            icolor = np.int_(normal(i0e[ib]) * nvalues) - 1
            if icolor < 0:
                icolor = 0
            if icolor >= nvalues:
                icolor = nvalues - 1
            ax.fill(xydata[:, 0], xydata[:, 1], color=cmap[icolor])
        else:
            ax.set_data(xydata[:, 0], xydata[:, 1])
        # plot x1 reflection
        # for j in range(its, ite) :
        j = ite  # One time slice
        for i in range(len(tdata)):
            xydata[i, :] = rl[j, ib, :] + np.cos(tdata[i]) * g1l[j, ib, :] + np.sin(tdata[i]) * g2l[j, ib, :]
        xydata[:, 0] = xydata[:, 0] + pi9 * (np.double(sl[j, ib]) + 0.5) * rmax

        if init == 1:
            (ax_polygon_plot_pol,) = ax.plot(xydata[:, 0], xydata[:, 1], color="0")
            icolor = np.int_(normal(i0[j, ib]) * nvalues) - 1
            if icolor < 0:
                icolor = 0
            if icolor >= nvalues:
                icolor = nvalues - 1
            ax.fill(xydata[:, 0], xydata[:, 1], color=cmap[icolor])
            # ax_polygon.plot(x, x**2, label='S'+str(i)+'_1')  # Plot more data on the axes...
            # ax_polygon.plot(x, x**3, label='cubic')  # ... and some more.
            # ax_polygon.set_xlabel('x label')  # Add an x-label to the axes.
            # ax_polygon.set_ylabel('y label')  # Add a y-label to the axes.
            # ax_polygon.set_title("Simple Plot")  # Add a title to the axes.
            # ax_polygon.legend();  # Add a legend.
            # invert both axes: focus on LFS
            ax.invert_xaxis()
            ax.invert_yaxis()
            # colorbar erzeugen
            cax, _ = cbar.make_axes(ax)
            cbar.ColorbarBase(cax, cmap=chosen_cmap, norm=normal)

            return ax_polygon_plot_pol
        else:
            ax.set_data(xydata[:, 0], xydata[:, 1])

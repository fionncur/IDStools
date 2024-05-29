import matplotlib.patches as patches
from matplotlib.path import Path
from idstools.compute.wall import WallCompute
import matplotlib.cm as cm


class WallView:
    def __init__(self, wall_ids):
        self.wall_ids = wall_ids
        self.computeObject = WallCompute(wall_ids)

    def addWallMarkings(self, ax, r, z, showLabels=False, **kwargs):
        """
        The function adds a path(Wall marking) to a given matplotlib axis object using the provided radial and vertical coordinates.

        Args:
            ax: The parameter "ax" is an instance of the Axes class in matplotlib. It represents the axes
        on which the patch will be added.
            r: The parameter "r" represents a list of x-coordinates for the vertices of the path.
            z: The parameter "z" represents the z-coordinates of the points in the path. It is a list or  array containing the z-coordinates of the points.
        """
        n = len(r)
        codes = [Path.MOVETO] + [Path.LINETO] * (n - 1)
        vertices = []
        for i in range(n):
            p = (r[i], z[i])
            vertices.append(p)

        path = Path(vertices, codes)
        patch = patches.PathPatch(path, **kwargs)
        if showLabels:
            ax.text(
                r[n - 1],
                z[n - 1],
                kwargs.get("label"),
                fontsize="x-small",
            )
        ax.add_patch(patch)

    def view_wall(self, ax, showLabels=False, **kwargs):
        """
        The function `view_wall` prints the values of `r` and `z` for each element in the `wall_data` dictionary and calls the `addWallMarkings` function to add a patch to the given `ax` object.

        Args:
            ax: `ax` is an instance of the `matplotlib.axes.Axes` class. It represents the axes on which
        the wall will be plotted.
            showLabels:shows labels on the plot
            kwargs: This is useful to update properties of patch (Wall marking on the plot). You can find it here https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html.. most useful are linewidth, linestyle, visible, animated, edgecolor, fill or facecolor
        """
        # These are the colors that will be used in the plot
        colors = [
            "#1f77b4",  # Blue
            "#ff7f0e",  # Orange
            "#2ca02c",  # Green
            "#d62728",  # Red
            "#9467bd",  # Purple
            "#8c564b",  # Brown
            "#e377c2",  # Pink
            "#7f7f7f",  # Gray
            "#bcbd22",  # Olive
            "#17becf",  # Cyan
            "#17a2b8",  # Teal
            "#b8e55d",  # Lime
            "#ff00ff",  # Magenta
            "#ffdd44",  # Yellow
            "#87ceeb",  # Sky Blue
            "#b57edc",  # Lavender
            "#40e0d0",  # Turquoise
            "#ffd700",  # Gold
            "#ff7f50",  # Coral
            "#dc143c",  # Crimson
        ]
        vIndex = 0
        if vesselUnits := self.computeObject.getVesselUnits():
            for _, description2d in vesselUnits.items():
                for vIndex, vesselUnit in description2d["vesselunits"].items():
                    showLabelFlag = True
                    vname = ""
                    if vesselUnit["identifier"]:
                        vname = vesselUnit["identifier"]
                    elif vesselUnit["name"]:
                        vname = vesselUnit["name"]
                    if vesselUnit["rectangle_coordinates"]:
                        for rw, zw in vesselUnit["rectangle_coordinates"]:
                            if showLabelFlag:
                                self.addWallMarkings(
                                    ax,
                                    rw,
                                    zw,
                                    showLabels=showLabels,
                                    label=vname,
                                    fill=False,
                                    color=colors[vIndex % 20],
                                    **kwargs,
                                )
                            else:
                                self.addWallMarkings(
                                    ax,
                                    rw,
                                    zw,
                                    fill=False,
                                    color=colors[vIndex % 20],
                                    **kwargs,
                                )
                            showLabelFlag = False

        if limiterUnits := self.computeObject.getLimiterUnits():
            for _, description2d in limiterUnits.items():

                for lIndex, limiterUnit in description2d["limiterunits"].items():
                    self.addWallMarkings(
                        ax,
                        limiterUnit["r"],
                        limiterUnit["z"],
                        showLabels=showLabels,
                        color=colors[(lIndex + vIndex + 1) % 20],
                        fill=False,
                        label=limiterUnit["name"],
                        **kwargs,
                    )
        ax.legend(
            bbox_to_anchor=(1.0, 0.5),
            loc="center left",
            borderaxespad=0.0,
            frameon=False,
            fontsize="x-small",
        )
        return True

import matplotlib.patches as patches
from matplotlib.path import Path

from idstools.compute.wall import WallCompute


class WallView:
    def __init__(self, wall_ids):
        self.wall_ids = wall_ids
        self.compute_object = WallCompute(wall_ids)

    def add_wall_markings(self, ax, r, z, show_labels=False, **kwargs):
        """
        The function adds a path(Wall marking) to a given matplotlib axis object using the provided radial and
        vertical coordinates.

        Args:
            ax: The parameter "ax" is an instance of the Axes class in matplotlib. It represents the axes
        on which the patch will be added.
            r: The parameter "r" represents a list of x-coordinates for the vertices of the path.
            z: The parameter "z" represents the z-coordinates of the points in the path. It is a list or  array
            containing the z-coordinates of the points.
        """
        n = len(r)
        codes = [Path.MOVETO] + [Path.LINETO] * (n - 1)
        vertices = []
        for i in range(n):
            p = (r[i], z[i])
            vertices.append(p)

        # check if vertices are empty
        if not vertices:
            print("Vertices are empty")
            return None

        # kwargs.setdefault("color", "darkgray")
        path = Path(vertices, codes)
        patch = patches.PathPatch(path, **kwargs)
        if show_labels:
            ax.text(
                r[n - 1],
                z[n - 1],
                kwargs.get("label"),
                fontsize="small",
                color="#333333",
            )
        ax.add_patch(patch)

    def view_wall_vessel(
        self,
        ax,
        select_description2d=":",
        select_unit=":",
        show_labels=False,
        wallcolor=None,
        **kwargs,
    ):
        """
        The function `view_wall` prints the values of `r` and `z` for each element in the `wall_data` dictionary
        and calls the `addWallMarkings` function to add a patch to the given `ax` object.

        Args:
            ax: `ax` is an instance of the `matplotlib.axes.Axes` class. It represents the axes on which
        the wall will be plotted.
            showLabels:shows labels on the plot
            kwargs: This is useful to update properties of patch (Wall marking on the plot). You can find it here
            https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html.. most useful are linewidth,
            linestyle, visible, animated, edgecolor, fill or facecolor
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
            "darkred",  # "#7f7f7f",  # Gray
            "#bcbd22",  # Olive
            "#17becf",  # Cyan
            "#17a2b8",  # Teal
            "darkblue",  # b8e55d",  # Lime
            "#ff00ff",  # Magenta
            "navy",  # "#ffdd44",  # Yellow
            "#87ceeb",  # Sky Blue
            "#b57edc",  # Lavender
            "#40e0d0",  # Turquoise
            "#ffd700",  # Gold
            "#ff7f50",  # Coral
            "darkgreen",  # dc143c",  # Crimson
        ]
        v_index = 0
        if vessel_units := self.compute_object.get_vessel_units(
            select_description2d=select_description2d, select_unit=select_unit
        ):
            for _, description2d in vessel_units.items():
                for v_index, vessel_unit in description2d["vesselunits"].items():
                    show_label_flag = True
                    vname = ""
                    if vessel_unit["name"]:
                        vname = vessel_unit["name"]
                    elif vessel_unit["identifier"]:
                        vname = vessel_unit["identifier"]
                    if wallcolor:
                        kwargs.update({"color": wallcolor})
                    else:
                        kwargs.update({"color": colors[v_index % 20]})
                    if vessel_unit["rectangle_coordinates"]:

                        for rw, zw in vessel_unit["rectangle_coordinates"]:
                            if show_label_flag:
                                self.add_wall_markings(
                                    ax,
                                    rw,
                                    zw,
                                    show_labels=show_labels,
                                    label=vname,
                                    fill=False,
                                    **kwargs,
                                )
                            else:
                                self.add_wall_markings(
                                    ax,
                                    rw,
                                    zw,
                                    fill=False,
                                    **kwargs,
                                )
                            show_label_flag = False
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, wall-vessel")
        else:
            ax.set_title("wall-vessel")

        return None

    def view_wall_limiter(
        self,
        ax,
        select_description2d=":",
        select_unit=":",
        show_labels=False,
        wallcolor=None,
        show_legend=False,
        **kwargs,
    ):
        colors = [
            "#1f77b4",  # Blue
            "#ff7f0e",  # Orange
            "#2ca02c",  # Green
            "#d62728",  # Red
            "#9467bd",  # Purple
            "#8c564b",  # Brown
            "#e377c2",  # Pink
            "darkred",  # "#7f7f7f",  # Gray
            "#bcbd22",  # Olive
            "#17becf",  # Cyan
            "#17a2b8",  # Teal
            "darkblue",  # b8e55d",  # Lime
            "#ff00ff",  # Magenta
            "navy",  # "#ffdd44",  # Yellow
            "#87ceeb",  # Sky Blue
            "#b57edc",  # Lavender
            "#40e0d0",  # Turquoise
            "#ffd700",  # Gold
            "#ff7f50",  # Coral
            "darkgreen",  # dc143c",  # Crimson
        ]
        v_index = 0
        if limiter_units := self.compute_object.get_limiter_units(
            select_description2d=select_description2d, select_unit=select_unit
        ):
            for _, description2d in limiter_units.items():

                for l_index, limiter_unit in description2d["limiterunits"].items():
                    if wallcolor:
                        kwargs.update({"color": wallcolor})
                    else:
                        kwargs.update({"color": colors[(l_index + v_index) % 20]})
                    self.add_wall_markings(
                        ax,
                        limiter_unit["r"],
                        limiter_unit["z"],
                        show_labels=show_labels,
                        fill=False,
                        label=limiter_unit["name"],
                        **kwargs,
                    )
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, wall-limiter")
        else:
            ax.set_title("wall-limiter")

        return None

    def view_inner_wall_line(self, ax):
        result = self.compute_object.get_inner_wall()
        if result is None:
            return None
        rw, zw = result
        ax.plot(rw, zw, linewidth=2, color="red")

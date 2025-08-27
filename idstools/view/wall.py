import matplotlib.patches as patches
import matplotlib.text as mtext
from matplotlib.patches import Rectangle
from matplotlib.path import Path

from idstools.compute.wall import WallCompute


class WallView:
    def __init__(self, wall_ids):
        self.wall_ids = wall_ids
        self.compute_object = WallCompute(wall_ids)

    def add_wall_markings(self, ax, r, z, **kwargs):
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
        if "label" in kwargs and not kwargs["label"]:
            kwargs["label"] = "wall"
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
        text = ax.text(r[n - 1], z[n - 1], kwargs.get("label"), fontsize="small", color="#333333", visible=False)
        ax.add_patch(patch)
        return patch, text

    def view_wall_vessel(
        self,
        ax,
        select_description2d=":",
        select_unit=":",
        wallcolor=None,
        **kwargs,
    ):
        """
        The function `view_wall` prints the values of `r` and `z` for each element in the `wall_data` dictionary
        and calls the `addWallMarkings` function to add a patch to the given `ax` object.

        Args:
            ax: `ax` is an instance of the `matplotlib.axes.Axes` class. It represents the axes on which
        the wall will be plotted.
            kwargs: This is useful to update properties of patch (Wall marking on the plot). You can find it here
            https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html.. most useful are linewidth,
            linestyle, visible, animated, edgecolor, fill or facecolor
        """
        # These are the colors that will be used in the plot
        colors = [
            "#001F3F",  # Deep Blue
            "#003366",  # Serene Blue
            "#0A192F",  # Twilight Blue
            "#1B3A4B",  # Dusky Blue
            "#004E89",  # Oceanic Blue
            "#003F5C",  # Marine Blue
            "#2C3E50",  # Starlit Blue
            "#102A43",  # Nocturnal Blue
            "#5B7C99",  # Frosty Blue
            "#6B8EAF",  # Icy Blue
            "#0F4C75",  # Sapphire Blue
            "#1B4965",  # Dreamy Blue
            "#3A506B",  # Calm Blue
            "#2E4A62",  # Tranquil Blue
            "#001B2E",  # Abyss Blue
            "#011F4B",  # Deepwater Blue
            "#34495E",  # Shadow Blue
            "#2C3A47",  # Evening Blue
            "#4B0082",  # Indigo
            "#281E5D",  # Deep Indigo
        ]
        v_index = 0
        if vessel_units := self.compute_object.get_vessel_units(
            select_description2d=select_description2d, select_unit=select_unit
        ):
            legend_map = {}
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
                        kwargs.update({"color": colors[v_index % 4]})
                    if vessel_unit["rectangle_coordinates"]:

                        for rw, zw in vessel_unit["rectangle_coordinates"]:
                            if show_label_flag:
                                shape, text = self.add_wall_markings(
                                    ax,
                                    rw,
                                    zw,
                                    label=f"wall/{vname}",
                                    fill=False,
                                    **kwargs,
                                )
                            else:
                                shape, text = self.add_wall_markings(
                                    ax,
                                    rw,
                                    zw,
                                    fill=False,
                                    **kwargs,
                                )
                            show_label_flag = False
                            legend_map[text] = shape

            def on_legend_click(event):
                legend = event.artist

                if isinstance(legend, mtext.Text) and "wall" in legend.get_text():
                    for text, scatter in legend_map.items():
                        if legend.get_text() == text.get_text():
                            font_weight = "bold" if not text.get_visible() else "normal"
                            legend.set_fontweight(font_weight)
                            text.set_visible(not text.get_visible())
                    ax.figure.canvas.draw_idle()
                elif isinstance(legend, Rectangle) and "wall" in legend.get_label():
                    for text, scatter in legend_map.items():
                        if legend.get_label() == text.get_text():
                            alpha_value = 1.0 if not scatter.get_visible() else 0.7
                            legend.set_alpha(alpha_value)
                            scatter.set_visible(not scatter.get_visible())

                    ax.figure.canvas.draw_idle()

            ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
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
        wallcolor=None,
        **kwargs,
    ):
        colors = [
            "#001F3F",  # Deep Blue
            "#003366",  # Serene Blue
            "#0A192F",  # Twilight Blue
            "#1B3A4B",  # Dusky Blue
            "#004E89",  # Oceanic Blue
            "#003F5C",  # Marine Blue
            "#2C3E50",  # Starlit Blue
            "#102A43",  # Nocturnal Blue
            "#5B7C99",  # Frosty Blue
            "#6B8EAF",  # Icy Blue
            "#0F4C75",  # Sapphire Blue
            "#1B4965",  # Dreamy Blue
            "#3A506B",  # Calm Blue
            "#2E4A62",  # Tranquil Blue
            "#001B2E",  # Abyss Blue
            "#011F4B",  # Deepwater Blue
            "#34495E",  # Shadow Blue
            "#2C3A47",  # Evening Blue
            "#4B0082",  # Indigo
            "#281E5D",  # Deep Indigo
        ]
        v_index = 0
        if limiter_units := self.compute_object.get_limiter_units(
            select_description2d=select_description2d, select_unit=select_unit
        ):
            legend_map = {}
            counter = 0
            for idescription2d, description2d in limiter_units.items():
                for l_index, limiter_unit in description2d["limiterunits"].items():
                    print(limiter_unit["name"])
                    if wallcolor:
                        kwargs.update({"color": wallcolor})
                    else:
                        kwargs.update({"color": colors[(l_index + v_index) % 4]})
                    shape, text = self.add_wall_markings(
                        ax,
                        limiter_unit["r"],
                        limiter_unit["z"],
                        fill=False,
                        label=(
                            f"wall/{limiter_unit['name']}" if limiter_unit["name"] != "" else f"wall/limiter{counter}"
                        ),
                        **kwargs,
                    )
                    counter = counter + 1
                    legend_map[text] = shape

            def on_legend_click(event):
                legend = event.artist

                if isinstance(legend, mtext.Text) and "wall" in legend.get_text():
                    for text, scatter in legend_map.items():
                        if legend.get_text() == text.get_text():
                            font_weight = "bold" if not text.get_visible() else "normal"
                            legend.set_fontweight(font_weight)
                            text.set_visible(not text.get_visible())
                    ax.figure.canvas.draw_idle()
                elif isinstance(legend, Rectangle) and "wall" in legend.get_label():
                    for text, scatter in legend_map.items():
                        if legend.get_label() == text.get_text():
                            alpha_value = 1.0 if not scatter.get_visible() else 0.7
                            legend.set_alpha(alpha_value)
                            scatter.set_visible(not scatter.get_visible())

                    ax.figure.canvas.draw_idle()

            ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
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
        ax.plot(rw, zw, color="red")

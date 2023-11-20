import matplotlib.patches as patches
from matplotlib.path import Path
from ..compute.wall import WallCompute


class WallView:
    def __init__(self, wall_ids):
        self.wall_ids = wall_ids
        self.wall_object = WallCompute(wall_ids)

    def addWallMarkings(self, ax, r, z, **kwargs):
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
        kwargs.setdefault("fill", False)
        patch = patches.PathPatch(path, **kwargs)
        ax.add_patch(patch)

    def view_wall(self, ax, **kwargs):
        """
        The function `view_wall` prints the values of `r` and `z` for each element in the `wall_data` dictionary and calls the `ax_add_rzpatch` function to add a patch to the given `ax` object.

        Args:
            ax: `ax` is an instance of the `matplotlib.axes.Axes` class. It represents the axes on which
        the wall will be plotted.
            kwargs: This is useful to update properties of patch (Wall marking on the plot). You can find it here https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.PathPatch.html.. most useful are linewidth, linestyle, visible, animated, edgecolor, fill or facecolor
        """
        if wall_data := self.wall_object.get_wall():
            for key, data in wall_data.items():
                if data:
                    for element_key, element_data in data.items():
                        r, z = element_data
                        self.addWallMarkings(ax, r, z, **kwargs)

        else:
            print("!  No Wall found")

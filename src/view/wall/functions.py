import matplotlib.patches as patches
from matplotlib.path import Path
from ...compute.wall.functions import WallCompute


class WallView:
    def __init__(self, wall_ids):
        self.wall_ids = wall_ids
        self.wall_object = WallCompute(wall_ids)

    def ax_add_rzpatch(self, ax, r, z, **kwargs):

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

    def view_wall(self, ax):
        wall_data = self.wall_object.get_wall()
        if not wall_data:
            print("!  No Wall found")
        else:
            for key, data in wall_data.items():
                for element_key, element_data in data.items():
                    r, z = element_data
                    print("r=", r, "z=", z)
                    self.ax_add_rzpatch(ax, r, z)

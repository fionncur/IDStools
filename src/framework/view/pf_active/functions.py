from matplotlib.patches import Rectangle
from ...compute import PFCoilsCompute


class PFCoilsPlot:
    def __init__(self, ax, ids_object):
        self.pfcoils_compute = PFCoilsCompute(ids_object)
        self.ax = ax

    def overlay(self):
        coils_data = self.pfcoils_compute.get_pf_coils()
        for coil_key, coil_data in coils_data.items():
            for element_key, element_data in coil_data.items():
                cew, ceh, cec = element_data
                rectangle = Rectangle(cec, cew, ceh)

                self.ax.add_patch(rectangle)
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width() / 2.0
                cy = ry + rectangle.get_height() / 2.0
                self.ax.annotate(
                    coil_key,
                    (cx, cy),
                    color="black",
                    weight="bold",
                    ha="center",
                    va="center",
                )

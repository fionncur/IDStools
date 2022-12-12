from matplotlib.patches import Rectangle


class PFCoilsPlot:
    def __init__(self, ax):
        self.ax = ax

    def overlay(self, coils_data):
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

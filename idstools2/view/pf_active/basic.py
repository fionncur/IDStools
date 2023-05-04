from matplotlib.patches import Rectangle
from ...compute.pf_active.basic import PFCoilsCompute


class PFCoilsView:
    def __init__(self, pf_ids):
        self.pf_ids = pf_ids
        self.pf_object = PFCoilsCompute(pf_ids)

    def view_pf_coils(self, ax):
        coils_data = self.pf_object.get_pf_coils()
        if not coils_data:
            print("!  No PF Coils found")
        else:
            for coil_key, coil_data in coils_data.items():
                for element_key, element_data in coil_data.items():
                    cew, ceh, cec = element_data
                    rectangle = Rectangle(cec, cew, ceh)

                    ax.add_patch(rectangle)
                    rx, ry = rectangle.get_xy()
                    cx = rx + rectangle.get_width() / 2.0
                    cy = ry + rectangle.get_height() / 2.0
                    ax.annotate(
                        coil_key,
                        (cx, cy),
                        color="black",
                        weight="bold",
                        ha="center",
                        va="center",
                    )

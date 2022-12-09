import numpy as np
import sys


class PFCoilsCompute:
    def __init__(self, ids_object):
        super().__init__()
        self.ids_object = ids_object

    def get_pf_coils(self):
        coils = {}
        for coil in self.ids_object.coil:
            element = {}
            element_counter = 0
            for element in coil.element:
                cew = element.geometry.rectangle.width
                ceh = element.geometry.rectangle.height
                if cew > 0.0 and ceh > 0.0:
                    cec = (
                        element.geometry.rectangle.r - cew / 2.0,
                        element.geometry.rectangle.z - ceh / 2.0,
                    )
                else:
                    cec = 0
                element["element" + element_counter] = (cew, ceh, cec)
                element_counter += 1
            coils[coil.identifier] = element
        return coils

        # rectangle = Rectangle(cec,cew,ceh)
        # ax.add_patch(rectangle)
        # rx, ry = rectangle.get_xy()
        # cx = rx + rectangle.get_width()/2.0
        # cy = ry + rectangle.get_height()/2.0
        # ax.annotate(coil.identifier, (cx, cy), color='black', weight='bold', ha='center', va='center')

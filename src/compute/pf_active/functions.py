class PFCoilsCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    @staticmethod
    def get_pf_coils(ids_object) -> dict:
        """
        Returns dictionary of pf coils and its data

        Returns:
            dict: [dictionary of pf coils and its data]
        """
        compute_object = PFCoilsCompute(ids_object)
        return compute_object.pf_coils()

    def pf_coils(self) -> dict:
        """
        Returns dictionary of pf coils and its data

        Returns:
            dict: [dictionary of pf coils and its data]
        """
        coils = {}

        for coil in self.ids_object.coil:
            element_dict = {}
            element_counter = 0
            for element in coil.element:
                cew = element.geometry.rectangle.width
                ceh = element.geometry.rectangle.height
                if cew > 0.0 and ceh > 0.0:
                    cec = (
                        element.geometry.rectangle.r - cew / 2.0,
                        element.geometry.rectangle.z - ceh / 2.0,
                    )
                    element_dict["element" + str(element_counter)] = (cew, ceh, cec)

                element_counter += 1
            coils[coil.identifier] = element_dict
        return coils

from ....domain.ecstray.functions import EcStrayCompute


class EcStrayView:
    def __init__(self, equilibrium_ids, core_profiles_ids, waves_ids):
        self.ecstray_object = EcStrayCompute(
            equilibrium_ids, core_profiles_ids, waves_ids
        )
        self.equilibrium_ids = equilibrium_ids
        self.core_profiles_ids = core_profiles_ids
        self.waves_ids = waves_ids

    def plot_resonance_layer(
        self, ax, time_index_wv, time_index_eq, init=1, verbose=False
    ):
        res_layer = self.ecstray_object.get_resonance_layer(
            time_index_wv, time_index_eq
        )

        for i_harm in range(len(res_layer)):
            if len(res_layer[i_harm]["r"]) > 1:
                if verbose == True:
                    print("Resonance at n = %i" % (i_harm + 1))
                if init == 1:
                    (ax_polview_plot_res,) = ax.plot(
                        res_layer[i_harm]["r"],
                        res_layer[i_harm]["z"],
                        color="r",
                        linewidth=2,
                    )
                    return ax_polview_plot_res
                else:
                    ax.set_data(res_layer[i_harm]["r"], res_layer[i_harm]["z"])

    def plot_cutoff_layer(
        self,
        ax,
        time_index_wv=0,
        time_index_cp=0,
        time_index_eq=0,
        init=1,
        verbose=False,
    ):
        # Calculate density cutoff layer position
        cutoff_layer = self.ecstray_object.get_cutoff_layer(
            time_index_wv, time_index_cp, time_index_eq
        )

        if init == 1:
            (ax_polview_plot_cut,) = ax.plot(
                cutoff_layer["r"], cutoff_layer["z"], color="g", linewidth=2
            )
            return ax_polview_plot_cut
        else:
            ax.set_data(cutoff_layer["r"], cutoff_layer["z"])

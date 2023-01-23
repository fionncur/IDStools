from ...view.common.functions import BasePlot
from ...compute.core_profiles.functions import CoreProfilesCompute


class CoreProfilesView:
    def __init__(self, ids_object):
        self.compute_object = CoreProfilesCompute(ids_object)
        self.ids_object = ids_object

    def plot_ne0(self, ax):
        ne0 = self.compute_object.get_ne0()
        time_array = self.ids_object.time

        ax.plot(time_array, ne0, color="r", label="$n_{e0} [10^{19}.m^{-3}]$")

        ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(ip)*1.2)
        ax.set_ylim(0, 20)

    def plot_density_profile(self, ax, time_index, psi_based=0, init=1):
        rho_tor_norm = self.compute_object.get_rho_tor_norm(time_index)

        psi = self.compute_object.get_psi(time_index)

        if rho_tor_norm is not None and psi is not None:
            radial_coordinate = rho_tor_norm
            xlabel = ""
            if init == 1:
                xlabel = r"Normalised $\rho_{tor}$ [-]"
            if psi_based == 1:
                radial_coordinate = psi
                if init == 1:
                    xlabel = r"$-\psi$ [Wb]"

            ax.set_xlabel(xlabel)
            electron_density = self.ids_object.profiles_1d[time_index].electrons.density
            nmax = max(electron_density) * 1.2
            ax_density_plot_dens = None
            if init == 1:
                (ax_density_plot_dens,) = ax.plot(
                    radial_coordinate,
                    electron_density,
                    color="b",
                    label=r"$n_e [m^{-3}]$",
                )
                # ax_density.set_ylim(bottom=0,top=max(electron_density))
            else:
                ax.legend(loc="upper right", shadow=True, fancybox=True)
                ax.set_ylim(top=nmax)
                ax.set_data(radial_coordinate, electron_density)
            return ax_density_plot_dens, nmax

from idstools.compute.equilibrium import EquilibriumCompute
from idstools.domain.ecstray import EcStrayCompute
import logging

# Font/Colour definition
fontsize = 9
bndcolor = "chocolate"
shotcolors = ["b", "r", "c", "y", "m", "b"]
shotstyle = ["-", "--", "-.", ":", ".", ","]
colorcounter = 0
lpad = -1

logger = logging.getLogger("module")


class EcStrayView:
    def __init__(self, equilibriumIds: object, coreProfilesIds: object, wavesIds: object):
        self.ecstray_object = EcStrayCompute(equilibriumIds, coreProfilesIds, wavesIds)
        self.equilibriumCompute = EquilibriumCompute(equilibriumIds)
        self.equilibriumIds = equilibriumIds
        self.coreProfilesIds = coreProfilesIds
        self.wavesIds = wavesIds

    def plotResonanceLayer(self, ax, time_index_wv, time_index_eq, init=1, verbose=False):
        """
        Plot the resonance layer on the given `ax` object.

        Args:
            ax (matplotlib.axes.Axes): The matplotlib Axes object on which the resonance layer will be plotted.
            time_index_wv (int): The time index for accessing wave-related data.
            time_index_eq (int): The time index for accessing equilibrium-related data.
            init (int): Indicates if the function is called for the initial setup. Set to 1 for initial setup.
            Default is 1.
            verbose (bool): Controls whether verbose output should be displayed. Default is False.

        Returns:
            matplotlib.lines.Line2D: The Line2D object representing the resonance layer plot.

        Example:
            .. code-block:: python

                from idstools.view.domain.ecstray import EcStrayView
                import imas
                from idstools.view.common import Canvas

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3", "r")
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                wavesIds = connection.get('waves')
                coreProfilesIds = connection.get('core_profiles')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="Resonance Layer", xlabel="R [m]", ylabel="Z [m]", row=0, col=0, rowspan=1)
                ax.set_title("uri=imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3")
                ecstrayView = EcStrayView(equilibriumIds, coreProfilesIds, wavesIds)
                ecstrayView.plotResonanceLayer(ax, time_index_wv=0, time_index_eq=0, verbose=True)

                ax.plot()
                canvas.show()

            .. thumbnail:: /_static/images/EcstrayView_plotResonanceLayer.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.domain.ecstray.EcStrayCompute.getResonanceLayer`

        """
        resultDict = self.ecstray_object.getResonanceLayer(time_index_wv, time_index_eq)
        res_layer = resultDict["resonanceLayer"]

        for i_harm in range(len(res_layer)):
            if len(res_layer[i_harm]["r"]) > 1:
                if verbose:
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

    def plotPoloidalView(self, ax, timeSlice=0):
        n_harm = [1, 2, 3, 4]

        resonanceData = self.ecstray_object.getResonanceLayer(nHarm=n_harm)
        profile2dIndex = resonanceData["profile2dIndex"]
        resonanceLayer = resonanceData["resonanceLayer"]

        gridData = self.equilibriumCompute.get2DCartesianGrid(timeSlice=timeSlice, profiles2DIndex=profile2dIndex)
        r2d = gridData["r2d"]
        z2d = gridData["z2d"]
        psi2d = gridData["psi2d"]
        rho2d = self.equilibriumCompute.getRho2D(timeSlice=timeSlice, profiles2DIndex=profile2dIndex)

        # Poloidal view plot
        ax.contour(r2d, z2d, psi2d, 50, cmap="summer")
        if len(rho2d) > 0:
            ax.contour(r2d, z2d, rho2d, 50, cmap="YlOrBr")
        # ax_polview.set_xlim(r2d.min(),r2d.max())
        ax.set_title("Poloidal view (R,Z)", fontsize=fontsize)
        ax.set_xlabel("R [m]", fontsize=fontsize, labelpad=lpad)
        ax.set_ylabel("Z [m]", fontsize=fontsize, labelpad=lpad)
        ax.set_xlim(3.4, r2d.max())
        ax.set_ylim(z2d.min() * 0.7, z2d.max() * 0.7)
        ax.set_aspect("equal", adjustable="box")
        for i_harm in range(len(n_harm)):
            if len(resonanceLayer[i_harm]["r"]) > 1:
                logger.info(f"Resonance at n = {i_harm}")
                ax.plot(
                    resonanceLayer[i_harm]["r"],
                    resonanceLayer[i_harm]["z"],
                    color="r",
                    linewidth=2,
                )

    def plotCutOffLayer(
        self,
        ax,
        timeIndexWaves=0,
        timeIndexCoreProfiles=0,
        timeIndexEquilibrium=0,
        init=1,
        verbose=False,
    ):
        """
        Plot the cutoff layer on the given `ax` object.

        Args:
            ax (matplotlib.axes.Axes): The matplotlib Axes object on which the cutoff layer will be plotted.
            timeIndexWaves (int): The time index for accessing wave-related data. Default is 0.
            timeIndexCoreProfiles (int): The time index for accessing core profile-related data. Default is 0.
            timeIndexEquilibrium (int): The time index for accessing equilibrium-related data. Default is 0.
            init (int): Indicates if the function is called for the initial setup. Set to 1 for initial setup.
            Default is 1.
            verbose (bool): Controls whether verbose output should be displayed. Default is False.

        Returns:
            matplotlib.lines.Line2D: The Line2D object representing the cutoff layer plot.

        Example:
            .. code-block:: python

                from idstools.view.domain.ecstray import EcStrayView
                import imas
                from idstools.view.common import Canvas

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3", "r")
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                wavesIds = connection.get('waves')
                coreProfilesIds = connection.get('core_profiles')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="Resonance Layer", xlabel="R [m]", ylabel="Z [m]", row=0, col=0, rowspan=1)
                ax.set_title("uri=imas:mdsplus?user=public;pulse=134173;run=2326;database=TEST;version=3")
                ecstrayView = EcStrayView(equilibriumIds, coreProfilesIds, wavesIds)
                ecstrayView.plotCutOffLayer(ax, timeIndexWaves=0, timeIndexCoreProfiles=0,
                timeIndexEquilibrium=0,verbose=True)

                ax.plot()
                canvas.show()

            .. thumbnail:: /_static/images/EcstrayView_plotCutOffLayer.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.domain.ecstray.EcStrayCompute.getCutoffLayer`
        """
        # Calculate density cutoff layer position
        cutoff_layer = self.ecstray_object.getCutoffLayer(timeIndexWaves, timeIndexCoreProfiles, timeIndexEquilibrium)

        # TODO Work on this function to keep call back function and events and not to pass init=1
        if init == 1:
            (ax_polview_plot_cut,) = ax.plot(cutoff_layer["r"], cutoff_layer["z"], color="g", linewidth=2)
            return ax_polview_plot_cut
        else:
            ax.set_data(cutoff_layer["r"], cutoff_layer["z"])

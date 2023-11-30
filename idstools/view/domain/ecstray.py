from idstools.domain.ecstray import EcStrayCompute


class EcStrayView:
    def __init__(
        self, equilibriumIds: object, coreProfilesIds: object, wavesIds: object
    ):
        self.ecstray_object = EcStrayCompute(equilibriumIds, coreProfilesIds, wavesIds)
        self.equilibriumIds = equilibriumIds
        self.coreProfilesIds = coreProfilesIds
        self.wavesIds = wavesIds

    def plotResonanceLayer(
        self, ax, time_index_wv, time_index_eq, init=1, verbose=False
    ):
        """
        Plot the resonance layer on the given `ax` object.

        Args:
            ax (matplotlib.axes.Axes): The matplotlib Axes object on which the resonance layer will be plotted.
            time_index_wv (int): The time index for accessing wave-related data.
            time_index_eq (int): The time index for accessing equilibrium-related data.
            init (int): Indicates if the function is called for the initial setup. Set to 1 for initial setup. Default is 1.
            verbose (bool): Controls whether verbose output should be displayed. Default is False.

        Returns:
            matplotlib.lines.Line2D: The Line2D object representing the resonance layer plot.

        Example:
            .. code-block:: python

                import imas
                # add necessary imports
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                coreProfilesIds = connection.get('waves')
                wavesIds = connection.get('core_profiles')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="Resonance Layer", xlabel="R [m]", ylabel="Z [m]", row=0, col=0, rowspan=1)

                ecstrayView = EcStrayView(equilibriumIds, coreProfilesIds, wavesIds)
                ecstrayView.plotResonanceLayer(ax, timeIndexWaves=0, timeIndexEquilibrium=0, verbose=True)

                ax.plot()
                canvas.show()

            .. image:: ../../_static/images/EcstrayView_plotResonanceLayer.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.domain.ecstray.EcStrayCompute.getResonanceLayer`

        """
        res_layer = self.ecstray_object.getResonanceLayer(time_index_wv, time_index_eq)
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
            init (int): Indicates if the function is called for the initial setup. Set to 1 for initial setup. Default is 1.
            verbose (bool): Controls whether verbose output should be displayed. Default is False.

        Returns:
            matplotlib.lines.Line2D: The Line2D object representing the cutoff layer plot.

        Example:
            .. code-block:: python

                import imas
                # add necessary imports
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                coreProfilesIds = connection.get('waves')
                wavesIds = connection.get('core_profiles')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="Cut Off Layer", xlabel="R [m]", ylabel="Z [m]", row=0, col=0, rowspan=1)

                ecstrayView = EcStrayView(equilibriumIds, coreProfilesIds, wavesIds)
                ecstrayView.plotCutOffLayer(ax, timeIndexWaves=0, timeIndexEquilibrium=0, verbose=True)

                ax.plot()
                canvas.show()

            .. image:: ../../_static/images/EcstrayView_plotCutOffLayer.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.domain.ecstray.EcStrayCompute.getCutoffLayer`
        """
        # Calculate density cutoff layer position
        cutoff_layer = self.ecstray_object.getCutoffLayer(
            timeIndexWaves, timeIndexCoreProfiles, timeIndexEquilibrium
        )

        # TODO Work on this function to keep call back function and events and not to pass init=1
        if init == 1:
            (ax_polview_plot_cut,) = ax.plot(
                cutoff_layer["r"], cutoff_layer["z"], color="g", linewidth=2
            )
            return ax_polview_plot_cut
        else:
            ax.set_data(cutoff_layer["r"], cutoff_layer["z"])

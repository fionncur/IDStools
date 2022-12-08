import matplotlib, os, sys

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt


class BasePlotLib:
    # Tick size and X and Y axes
    ticksize = 15

    # Font definition
    font = {
        "family": "serif",
        "color": "darkred",
        "weight": "normal",
        "size": 18,
    }

    fig_size_width = 4.5
    fig_size_height = 6.5
    fig_save_dpi = 100

    def __init__(self, data=None) -> None:
        self.validate_data(data)
        self.data = data
        self.fig, self.ax = plt.subplots()

    def validate_data(self, data):
        return True

    def save(self):
        fig = plt.gcf()
        fig.set_size_inches(BasePlotLib.fig_size_width, BasePlotLib.fig_size_height)
        try:
            fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
                self.data["shot"], self.data["run"], self.data["time"]
            )
            fig.savefig(fname, dpi=BasePlotLib.fig_save_dpi)
            print("----> Figure saved to " + fname, file=sys.stderr)
        except:
            print(
                "The figure could not be saved (check local permissions).",
                file=sys.stderr,
            )

    def show(self):
        plt.show()


class EquilibriumPlotDataInterface:
    def __init__(self) -> None:
        self.r2d = None
        self.z2d = None
        self.rho2d = None
        self.psi2d = None
        self.time = None
        self.hostdir = None
        self.shot = None
        self.run = None
        self.plotrho = None
        self.allInfo = None
        self.levels = None


class EquilibriumPlot(BasePlotLib):
    def __init__(self, data):
        super().__init__(data)  # expects EquilibriumPlotDataInterface type
        # Display the figure

        self.r2d = data.r2d
        self.z2d = data.z2d
        self.rho2d = data.rho2d
        self.psi2d = data.psi2d
        self.time = data.time
        self.hostdir = data.hostdir
        self.shot = data.shot
        self.run = data.run
        self.plotrho = data.plotrho
        self.allInfo = data.allInfo
        self.levels = data.levels

    def set_plot(self):
        if self.plotrho:

            plt.contour(self.r2d, self.z2d, self.rho2d, self.levels, colors="r")
        plt.contour(self.r2d, self.z2d, self.psi2d, self.levels)
        plt.xlim(self.r2d.min(), self.r2d.max())
        plt.gca().set_aspect("equal", adjustable="box")
        plt.xlabel("$R$ [m]", fontdict=BasePlotLib.font)
        plt.ylabel("$Z$ [m]", fontdict=BasePlotLib.font)
        plt.xticks(fontsize=BasePlotLib.ticksize)
        plt.yticks(fontsize=BasePlotLib.ticksize)
        plottitle = "2D equilibrium"
        if self.allInfo:
            plottitle += " (t={:.3f})".format(self.time)
        plt.title(plottitle, fontdict=BasePlotLib.font)

        if self.allInfo:
            self.set_info()
        # from matplotlib.offsetbox import AnchoredText
        # anchored_text = AnchoredText('Shot '+str(shot)+' / '+'Run '+str(run),prop=dict(size=8),loc=4)
        # ax.add_artist(anchored_text)

    def set_info(self):
        ax = plt.gca()

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.text(
            xmax + 0.01 * abs(xmax),
            ymin + 0.5 * abs(ymax - ymin),
            "{0}-Shot:{1},{2}".format(self.hostdir, self.shot, self.run),
            horizontalalignment="left",
            verticalalignment="center",
            rotation="vertical",
            fontsize=7,
        )


# if __name__ == "__main__":
#     pass
#     parser = argparse.ArgumentParser(
#         description="---- Display the plasma equilibrium from the equilibrium IDS",
#         parents=[imas_parser],
#     )
#     parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
#     parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
#     parser.add_argument(
#         "-t", "--time", help="Time (default=middle)", type=float, default=-99.0
#     )
#     parser.add_argument(
#         "-o",
#         "--occurrence",
#         help="Occurrence number (default=%(default)s)",
#         type=int,
#         default=0,
#     )
#     parser.add_argument("-p", "--plotrho", help="Plots rho(R,Z)", action="store_true")
#     parser.add_argument(
#         "-a",
#         "--allInfo",
#         help="Adds all extra provenance info to the plot",
#         action="store_true",
#     )

#     args = parser.parse_args()

#     dataproviderCommon = DataProviderCommon(
#         database=args.database,
#         backend=args.backend,
#         shot=args.shot,
#         run=args.run,
#         user=args.user,
#     )
#     ids_name = "equilibrium"
#     ids_object = dataproviderCommon.get_ids(ids_name)
#     hostdir = dataproviderCommon.get_database_path(args.database, args.user)
#     # Create ids object
#     equilibriumLib = EquilibriumLib(ids_object)

#     # Fill time series
#     ids_object.time = dataproviderCommon.get_time(ids_name, args.occurrence)
#     if ids_object.time is None:
#         print(
#             "The "
#             + ids_name
#             + " IDS for this occurence is empty in the input"
#             + " data-entry because "
#             + ids_name
#             + ".time is empty",
#             file=sys.stderr,
#         )
#         exit()
#     # Calculate time index for time of interest
#     time_index, time_value = equilibriumLib.calculate_time_index(args.time)

#     # Ask for time slice
#     ids_object.time_slice.resize(1)
#     ids_object.time_slice[0] = dataproviderCommon.get_time_slice(
#         ids_name, time_index, args.occurrence
#     )
#     print(ids_object)
#     equilibriumLib.validate_2d_profile()
#     calculationdata = equilibriumLib.get_cartesian_r_z_grids()

#     plot_data = AttrDict()
#     plot_data["time"] = ids_object.time
#     plot_data["hostdir"] = dataproviderCommon.database_path
#     plot_data["shot"] = args.shot
#     plot_data["run"] = args.run
#     plot_data["plotrho"] = calculationdata["plotrho"]
#     plot_data["shot"] = args.shot
#     plot_data["run"] = args.run
#     plot_data["user"] = args.user

#     plot_data["r2d"] = calculationdata["r2d"]
#     plot_data["z2d"] = calculationdata["z2d"]
#     plot_data["rho2d"] = calculationdata["rho2d"]
#     plot_data["psi2d"] = calculationdata["psi2d"]
#     plot_data["allInfo"] = args.allInfo
#     plot_data["levels"] = 30
#     plot_data.r2d = calculationdata["r2d"]
#     print(plot_data.r2d)
#     equilibriumPlot = EquilibriumPlot(plot_data)
#     equilibriumPlot.set_plot()
#     equilibriumPlot.set_info()
#     equilibriumPlot.show()

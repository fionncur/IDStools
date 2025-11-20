import logging
import os
import sys

import matplotlib

# Always use non-GUI backend in headless environments or when tkinter is not available
if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    # Check if tkinter is available
    try:
        import tkinter  # noqa: F401 - imported to check availability

        matplotlib.use("TkAgg")
    except (ImportError, ModuleNotFoundError):
        # tkinter not available, use non-GUI backend
        matplotlib.use("agg")

import matplotlib.pyplot as plt

logger = logging.getLogger("module")

current_directory = os.path.abspath(os.path.dirname(__file__))
# reach to `share` directory (sys.prefix won't work if using --prefix option)
share_directory = os.path.abspath(os.path.join(current_directory, "../../../../../"))
mplstyle_filepath = os.path.join(share_directory, r"share/styles/scientific.mplstyle")

if os.path.exists(mplstyle_filepath):
    plt.style.use(mplstyle_filepath)
else:
    plt.style.use(os.path.join(current_directory, r"styles/scientific.mplstyle"))


try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.pretty import Pretty, pprint

    rich_available = True
except ImportError:
    rich_available = False


class PlotCanvas:
    # https://matplotlib.org/stable/tutorials/intermediate/arranging_axes.html

    def __init__(self, nrows=1, ncols=1, *args, **kwargs) -> None:
        # self.fig, self.axes_array = plt.subplots(nrows, ncols)
        self.nrows = nrows
        self.ncols = ncols
        self.fig = plt.figure(*args, **kwargs)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5)

    # Share axes
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html#sphx-glr-gallery-subplots-axes-and-figures-shared-axis-demo-py
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/share_axis_lims_views.html#sphx-glr-gallery-subplots-axes-and-figures-share-axis-lims-views-py
    def add_axes(
        self,
        title=None,
        xlabel=None,
        ylabel=None,
        row=0,
        col=0,
        rowspan=1,
        colspan=1,
        **kwargs,
    ):
        ax = plt.subplot2grid(
            shape=(self.nrows, self.ncols),
            loc=(row, col),
            rowspan=rowspan,
            colspan=colspan,
            fig=self.fig,
            **kwargs,
        )
        if title is not None:
            ax.set_title(title)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        return ax

    def save(
        self,
        fname,
        width=11.69,
        height=8.27,
        dpi="figure",
    ):
        fig = plt.gcf()
        fig.set_size_inches(width, height)
        try:
            fig.savefig(fname, dpi=dpi)
            print(f"----> Figure saved to {fname}", file=sys.stderr)
        except Exception as e:
            logger.debug(f"{e}")

    def set_text(self, x=0.001, y=0.985, text="", ha="left", fontsize=7):
        plt.figtext(
            x,
            y,
            text,
            ha=ha,
            fontsize=fontsize,
        )

    def set_sup_title(self, text="", *args, **kwargs):
        plt.suptitle(text, *args, **kwargs)

    def show(self, *args, **kwargs):
        wm = self.get_current_fig_manager()
        window = wm.window
        screen_y = window.winfo_screenheight()
        screen_x = window.winfo_screenwidth()
        wm.resize(screen_x, screen_y)
        plt.show(*args, **kwargs)

    def get_current_fig_manager(self):
        return plt.get_current_fig_manager()

    @staticmethod
    def is_axes_empty(ax):
        """
        Check if a given Matplotlib Axes object is empty.

        An Axes object is considered empty if it has no data, no lines, no patches, and no texts.

        Parameters:
        ax (matplotlib.axes.Axes): The Axes object to check.

        Returns:
        bool: True if the Axes object is empty, False otherwise.
        """
        return not ax.has_data() and len(ax.lines) == 0 and len(ax.patches) == 0 and len(ax.texts) == 0

    def remove_empty_axes(self):
        """
        Remove empty axes from the figure.

        This method iterates over all axes in the figure and removes those that are empty.
        An axis is considered empty if the `PlotCanvas.is_axes_empty` method returns True.

        Returns:
            None
        """
        for ax in self.fig.axes[:]:  # Iterate over a copy of the axes list
            if PlotCanvas.is_axes_empty(ax):
                self.fig.delaxes(ax)

    def set_style(self, style="default"):
        """
        The function `setStyle` in allows you to set different color schemes for plots using Matplotlib based
        on the specified style parameter. Available styles are vibrant, retro, muted, high-vis, contrast, bright

        Args:
            style: The `setStyle` function allows you to set different color schemes for your plots based on the
                `style` parameter you provide. Defaults to default
        """
        if style == "default":
            # Standard SciencePlots color cycle

            # Set color cycle: blue, green, yellow, red, violet, gray
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                ["0C5DA5", "00B945", "FF9500", "FF2C00", "845B97", "474747", "9e9e9e"],
            )
        if style == "vibrant":
            # Vibrant color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                ["EE7733", "0077BB", "33BBEE", "EE3377", "CC3311", "009988", "BBBBBB"],
            )
        if style == "retro":
            # Retro color style

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color", ["4165c0", "e770a2", "5ac3be", "696969", "f79a1e", "ba7dcd"]
            )
        if style == "muted":
            # Muted color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                [
                    "CC6677",
                    "332288",
                    "DDCC77",
                    "117733",
                    "88CCEE",
                    "882255",
                    "44AA99",
                    "999933",
                    "AA4499",
                    "DDDDDD",
                ],
            )
        if style == "light":
            # Light color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                [
                    "77AADD",
                    "EE8866",
                    "EEDD88",
                    "FFAABB",
                    "99DDFF",
                    "44BB99",
                    "BBCC33",
                    "AAAA00",
                    "DDDDDD",
                ],
            )

        if style == "high-vis":
            # Matplotlib style for high visability plots (i.e., bright colors!!!)

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color", ["0d49fb", "e6091c", "26eb47", "8936df", "fec32d", "25d7fd"]
            ) + matplotlib.cycler("ls", ["-", "--", "-.", ":", "-", "--"])

        if style == "contrast":
            # High-contrast color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler("color", ["004488", "DDAA33", "BB5566"])

        if style == "bright":
            # Bright color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                ["4477AA", "EE6677", "228833", "CCBB44", "66CCEE", "AA3377", "BBBBBB"],
            )

    def update_style(self, param_string=""):
        """
        Updates matplotlib rcParams using a semicolon-separated string.
        Example input: "lines.linewidth=2;axes.titlesize=16"
        """
        for item in param_string.split(";"):
            if not item.strip():
                continue
            try:
                key, value = item.split("=", 1)
                key = key.strip()
                value = eval(value.strip(), {}, {})  # Convert to actual Python type
                matplotlib.rcParams[key] = value
            except Exception as e:
                print(f"Error applying rcParam '{item}': {e}")


class BasePlot:
    def database_info(self, ax, title, hostdir, shot, run, t):
        plottitle = title
        plottitle += " (t={:.3f})".format(t)
        ax.set_title(plottitle)

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        ax.text(
            xmax + 0.01 * abs(xmax),
            ymin + 0.5 * abs(ymax - ymin),
            "{0}-Shot:{1},{2}".format(hostdir, shot, run),
            horizontalalignment="left",
            verticalalignment="center",
            rotation="vertical",
            fontsize=7,
        )


class Terminal:
    tabsize = 10
    TAB = " " * 16
    LINE = "-" * 8

    def __init__(self) -> None:
        if rich_available:
            self.console = Console()

    def print(self, text, style=None, panel=False, pretty=False):
        if type(text) is dict:
            pprint(text, expand_all=True)
            return
        if style is None:
            style = "green"
        if rich_available:
            if pretty:
                text = Pretty(text)
            if panel:
                text = Panel(text)
            self.console.print(text, style=style, highlight=False)
            return
        print(text)

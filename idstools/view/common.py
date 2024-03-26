import os
import sys

import matplotlib

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt

# fsize = 8
# tsize = 10
# tdir = "in"
# major = 5.0
# minor = 3.0
# lwidth = 0.8
# lhandle = 2.0
# plt.style.use("default")
# # plt.rcParams["text.usetex"] = True
# plt.rcParams["font.size"] = fsize
# plt.rcParams["legend.fontsize"] = tsize
# plt.rcParams["xtick.direction"] = tdir
# plt.rcParams["ytick.direction"] = tdir
# plt.rcParams["xtick.major.size"] = major
# plt.rcParams["xtick.minor.size"] = minor
# plt.rcParams["ytick.major.size"] = 5.0
# plt.rcParams["ytick.minor.size"] = 3.0
# plt.rcParams["axes.linewidth"] = lwidth
# plt.rcParams["legend.handlelength"] = lhandle

# plt.rcParams["lines.linewidth"] = 1

current_directory = os.path.abspath(os.path.dirname(__file__))
# reach to `share` directory (sys.prefix won't work if using --prefix option)
share_directory = os.path.abspath(os.path.join(current_directory, "../../../../../"))
mplstyle_filepath = os.path.join(share_directory, r"share/styles/scientific.mplstyle")

if os.path.exists(mplstyle_filepath):
    plt.style.use(os.path.join(mplstyle_filepath))
else:
    mplstyle_filepath = os.path.join(current_directory, r"styles/scientific.mplstyle")
    plt.style.use(os.path.join(mplstyle_filepath))
import logging
import math
import weakref

import matplotlib.pyplot as _plt
import numpy

try:
    import rich
    from rich.console import Console
    from rich.panel import Panel
    from rich.pretty import Pretty, pprint

    richAvailable = True
except ImportError:
    richAvailable = False


class MplInteraction(object):
    """Base class for class providing interaction to a matplotlib Figure."""

    def __init__(self, figure):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        """
        self._fig_ref = weakref.ref(figure)
        self._cids = []

    def __del__(self):
        self.disconnect()

    def _add_connection(self, event_name, callback):
        """Called to add a connection to an event of the figure
        :param str event_name: The matplotlib event name to connect to.
        :param callback: The callback to register to this event.
        """
        cid = self.figure.canvas.mpl_connect(event_name, callback)
        self._cids.append(cid)

    def disconnect(self):
        """Disconnect interaction from Figure."""
        if self._fig_ref is not None:
            figure = self._fig_ref()
            if figure is not None:
                for cid in self._cids:
                    figure.canvas.mpl_disconnect(cid)
            self._fig_ref = None

    @property
    def figure(self):
        """The Figure this interaction is connected to or
        None if not connected."""
        return self._fig_ref() if self._fig_ref is not None else None

    def _axes_to_update(self, event):
        """Returns two sets of Axes to update according to event.
        Takes care of multiple axes and shared axes.
        :param MouseEvent event: Matplotlib event to consider
        :return: Axes for which to update xlimits and ylimits
        :rtype: 2-tuple of set (xaxes, yaxes)
        """
        x_axes, y_axes = set(), set()

        # Go through all axes to enable zoom for multiple axes subplots
        for ax in self.figure.axes:
            if ax.contains(event)[0]:
                # For twin x axes, makes sure the zoom is applied once
                shared_x_axes = set(ax.get_shared_x_axes().get_siblings(ax))
                if x_axes.isdisjoint(shared_x_axes):
                    x_axes.add(ax)

                # For twin y axes, makes sure the zoom is applied once
                shared_y_axes = set(ax.get_shared_y_axes().get_siblings(ax))
                if y_axes.isdisjoint(shared_y_axes):
                    y_axes.add(ax)

        return x_axes, y_axes

    def _draw(self):
        """Conveninent method to redraw the figure"""
        self.figure.canvas.draw()


class ZoomOnWheel(MplInteraction):
    """Class providing zoom on wheel interaction to a matplotlib Figure.
    Supports subplots, twin Axes and log scales.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(ZoomOnWheel, self).__init__(figure)
        self._add_connection("scroll_event", self._on_mouse_wheel)

        self.scale_factor = scale_factor

    @staticmethod
    def _zoom_range(begin, end, center, scale_factor, scale):
        """Compute a 1D range zoomed around center.
        :param float begin: The begin bound of the range.
        :param float end: The end bound of the range.
        :param float center: The center of the zoom (i.e., invariant point)
        :param float scale_factor: The scale factor to apply.
        :param str scale: The scale of the axis
        :return: The zoomed range (min, max)
        """
        if begin < end:
            min_, max_ = begin, end
        else:
            min_, max_ = end, begin

        if scale == "linear":
            old_min, old_max = min_, max_
        elif scale == "log":
            old_min = numpy.log10(min_ if min_ > 0.0 else numpy.nextafter(0, 1))
            center = numpy.log10(center if center > 0.0 else numpy.nextafter(0, 1))
            old_max = numpy.log10(max_) if max_ > 0.0 else 0.0
        else:
            logging.warning('Zoom on wheel not implemented for scale "%s"' % scale)
            return begin, end

        offset = (center - old_min) / (old_max - old_min)
        range_ = (old_max - old_min) / scale_factor
        new_min = center - offset * range_
        new_max = center + (1.0 - offset) * range_

        if scale == "log":
            try:
                new_min, new_max = 10.0 ** float(new_min), 10.0 ** float(new_max)
            except OverflowError:  # Limit case
                new_min, new_max = min_, max_
            if new_min <= 0.0 or new_max <= 0.0:  # Limit case
                new_min, new_max = min_, max_

        if begin < end:
            return new_min, new_max
        else:
            return new_max, new_min

    def _on_mouse_wheel(self, event):
        if event.step > 0:
            scale_factor = self.scale_factor
        else:
            scale_factor = 1.0 / self.scale_factor

        # Go through all axes to enable zoom for multiple axes subplots
        x_axes, y_axes = self._axes_to_update(event)

        for ax in x_axes:
            transform = ax.transData.inverted()
            xdata, ydata = transform.transform_point((event.x, event.y))

            xlim = ax.get_xlim()
            xlim = self._zoom_range(
                xlim[0], xlim[1], xdata, scale_factor, ax.get_xscale()
            )
            ax.set_xlim(xlim)

        for ax in y_axes:
            ylim = ax.get_ylim()
            ylim = self._zoom_range(
                ylim[0], ylim[1], ydata, scale_factor, ax.get_yscale()
            )
            ax.set_ylim(ylim)

        if x_axes or y_axes:
            self._draw()


class PanAndZoom(ZoomOnWheel):
    """Class providing pan & zoom interaction to a matplotlib Figure.
    Left button for pan, right button for zoom area and zoom on wheel.
    Support subplots, twin Axes and log scales.
    """

    def __init__(self, figure=None, scale_factor=1.1):
        """Initializer
        :param Figure figure: The matplotlib figure to attach the behavior to.
        :param float scale_factor: The scale factor to apply on wheel event.
        """
        super(PanAndZoom, self).__init__(figure, scale_factor)
        self._add_connection("button_press_event", self._on_mouse_press)
        self._add_connection("button_release_event", self._on_mouse_release)
        self._add_connection("motion_notify_event", self._on_mouse_motion)

        self._pressed_button = None  # To store active button
        self._axes = None  # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction

    @staticmethod
    def _pan_update_limits(ax, axis_id, event, last_event):
        """Compute limits with applied pan."""
        assert axis_id in (0, 1)
        if axis_id == 0:
            lim = ax.get_xlim()
            scale = ax.get_xscale()
        else:
            lim = ax.get_ylim()
            scale = ax.get_yscale()

        pixel_to_data = ax.transData.inverted()
        data = pixel_to_data.transform_point((event.x, event.y))
        last_data = pixel_to_data.transform_point((last_event.x, last_event.y))

        if scale == "linear":
            delta = data[axis_id] - last_data[axis_id]
            new_lim = lim[0] - delta, lim[1] - delta
        elif scale == "log":
            try:
                delta = math.log10(data[axis_id]) - math.log10(last_data[axis_id])
                new_lim = [
                    pow(10.0, (math.log10(lim[0]) - delta)),
                    pow(10.0, (math.log10(lim[1]) - delta)),
                ]
            except (ValueError, OverflowError):
                new_lim = lim  # Keep previous limits
        else:
            logging.warning('Pan not implemented for scale "%s"' % scale)
            new_lim = lim
        return new_lim

    def _pan(self, event):
        if event.name == "button_press_event":  # begin pan
            self._event = event

        elif event.name == "button_release_event":  # end pan
            self._event = None

        elif event.name == "motion_notify_event":  # pan
            if self._event is None:
                return

            if event.x != self._event.x:
                for ax in self._axes[0]:
                    xlim = self._pan_update_limits(ax, 0, event, self._event)
                    ax.set_xlim(xlim)

            if event.y != self._event.y:
                for ax in self._axes[1]:
                    ylim = self._pan_update_limits(ax, 1, event, self._event)
                    ax.set_ylim(ylim)

            if event.x != self._event.x or event.y != self._event.y:
                self._draw()

            self._event = event

    def _zoom_area(self, event):
        if event.name == "button_press_event":  # begin drag
            self._event = event
            self._patch = _plt.Rectangle(
                xy=(event.xdata, event.ydata),
                width=0,
                height=0,
                fill=False,
                linewidth=1.0,
                linestyle="solid",
                color="black",
            )
            self._event.inaxes.add_patch(self._patch)

        elif event.name == "button_release_event":  # end drag
            self._patch.remove()
            del self._patch

            if abs(event.x - self._event.x) < 3 or abs(event.y - self._event.y) < 3:
                return  # No zoom when points are too close

            x_axes, y_axes = self._axes

            for ax in x_axes:
                pixel_to_data = ax.transData.inverted()
                begin_pt = pixel_to_data.transform_point((event.x, event.y))
                end_pt = pixel_to_data.transform_point((self._event.x, self._event.y))

                min_ = min(begin_pt[0], end_pt[0])
                max_ = max(begin_pt[0], end_pt[0])
                if not ax.xaxis_inverted():
                    ax.set_xlim(min_, max_)
                else:
                    ax.set_xlim(max_, min_)

            for ax in y_axes:
                pixel_to_data = ax.transData.inverted()
                begin_pt = pixel_to_data.transform_point((event.x, event.y))
                end_pt = pixel_to_data.transform_point((self._event.x, self._event.y))

                min_ = min(begin_pt[1], end_pt[1])
                max_ = max(begin_pt[1], end_pt[1])
                if not ax.yaxis_inverted():
                    ax.set_ylim(min_, max_)
                else:
                    ax.set_ylim(max_, min_)

            self._event = None

        elif event.name == "motion_notify_event":  # drag
            if self._event is None:
                return

            if event.inaxes != self._event.inaxes:
                return  # Ignore event outside plot

            self._patch.set_width(event.xdata - self._event.xdata)
            self._patch.set_height(event.ydata - self._event.ydata)

        self._draw()

    def _on_mouse_press(self, event):
        if self._pressed_button is not None:
            return  # Discard event if a button is already pressed

        if event.button in (1, 3):  # Start
            x_axes, y_axes = self._axes_to_update(event)
            if x_axes or y_axes:
                self._axes = x_axes, y_axes
                self._pressed_button = event.button

                if self._pressed_button == 1:  # pan
                    self._pan(event)
                elif self._pressed_button == 3:  # zoom area
                    self._zoom_area(event)

    def _on_mouse_release(self, event):
        if self._pressed_button == event.button:
            if self._pressed_button == 1:  # pan
                self._pan(event)
            elif self._pressed_button == 3:  # zoom area
                self._zoom_area(event)
            self._pressed_button = None

    def _on_mouse_motion(self, event):
        if self._pressed_button == 1:  # pan
            self._pan(event)
        elif self._pressed_button == 3:  # zoom area
            self._zoom_area(event)


def figure_pz(*args, **kwargs):
    """matplotlib.pyplot.figure with pan and zoom interaction"""
    fig = _plt.figure(*args, **kwargs)
    fig.pan_zoom = PanAndZoom(fig)
    return fig


class Canvas:
    # https://matplotlib.org/stable/tutorials/intermediate/arranging_axes.html

    def __init__(self, nrows=1, ncols=1, *args, **kwargs) -> None:
        # self.fig, self.axes_array = plt.subplots(nrows, ncols)
        self.nrows = nrows
        self.ncols = ncols
        self.fig = figure_pz(*args, **kwargs)
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
        ax.grid()
        return ax

    def save(
        self,
        fname,
        width=None,
        height=None,
        dpi="figure",
    ):
        fig = plt.gcf()
        if width is not None and height is not None:
            fig.set_size_inches(width, height)
        try:
            fig.savefig(fname, dpi=dpi)
            print(f"----> Figure saved to {fname}", file=sys.stderr)
        except Exception as e:
            print(
                e,
                file=sys.stderr,
            )

    def setText(self, x=0.5, y=0.01, text=""):
        plt.figtext(
            0.5,
            0.01,
            text,
            ha="center",
            fontsize=7,
        )

    def setSupTitle(self, text="", *args, **kwargs):
        plt.suptitle(text, *args, **kwargs)

    def show(self, *args, **kwargs):
        plt.show(*args, **kwargs)

    def get_current_fig_manager(self):
        return plt.get_current_fig_manager()

    def setStyle(self, style="default"):
        """
        The function `setStyle` in allows you to set different color schemes for plots using Matplotlib based on the specified style parameter. Available styles are vibrant, retro, muted, high-vis, contrast, bright

        Args:
            style: The `setStyle` function allows you to set different color schemes for your plots based on the `style` parameter you provide. Defaults to default
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
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color", ["004488", "DDAA33", "BB5566"]
            )

        if style == "bright":
            # Bright color scheme
            # color-blind safe
            # from Paul Tot's website: https://personal.sron.nl/~pault/

            # Set color cycle
            matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(
                "color",
                ["4477AA", "EE6677", "228833", "CCBB44", "66CCEE", "AA3377", "BBBBBB"],
            )


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
        # from matplotlib.offsetbox import AnchoredText

        # anchored_text = AnchoredText(
        #     "Shot " + str(shot) + " / " + "Run " + str(run), prop=dict(size=8), loc=4
        # )
        # self.ax.add_artist(anchored_text)


class Terminal:
    tabsize = 10
    TAB = " " * 16
    LINE = "-" * 8

    def __init__(self) -> None:
        if richAvailable:
            self.console = Console()

    def print(self, text, style=None, panel=False, pretty=False):
        if type(text) is dict:
            pprint(text, expand_all=True)
            return
        if style is None:
            style = "green"
        if richAvailable:
            if pretty:
                text = Pretty(text)
            if panel:
                text = Panel(text)
            self.console.print(text, style=style, highlight=False)
            return
        print(text)

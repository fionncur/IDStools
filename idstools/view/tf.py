"""
This module provides view functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
import matplotlib.text as mtext
import numpy as np
from matplotlib.patches import Patch, Polygon
from scipy.interpolate import splprep, splev

from idstools.compute.tf import TFCompute

logger = logging.getLogger(__name__)


class TFView:
    """This class provides view functions for tf ids"""

    def __init__(self, ids: object):
        """Initialization TFView object.

        Args:
            ids : tf ids object
        """
        self.ids = ids
        self.compute_obj = TFCompute(ids)

    def view_tf_coils(
        self,
        ax: plt.axes,
        select_coil=":",
        select_conductor=":",
        color="#57b6ed",
        edgecolor="#0000ff",
        facecolor="#57b6ed",
        alpha=0.7,
    ):
        """
        Plots the Toroidal Field (TF) coils on the given matplotlib axis.

        Parameters:
        ax (plt.axes): The matplotlib axis to plot on.
        select_coil (str, optional): The coil selection criteria. Defaults to ":".
        select_conductor (str, optional): The conductor selection criteria. Defaults to "".
        color (str, optional): The color to use for plotting the coils. Defaults to "#800000".

        Returns:
        Patch: A matplotlib Patch object for the TF legend.

        Notes:
        - The function retrieves TF coil data using the compute_obj's get_tf_coils method.
        - If no TF coil data is found, a warning is logged and the function returns without plotting.
        - The function plots the start and end points of the coil conductors and connects them with line segments.
        - The aspect ratio of the plot is set to be equal and the title is updated to include "tf".
        """
        coils_dict = self.compute_obj.get_tf_coils(select_coil=select_coil, select_conductor=select_conductor)

        if coils_dict is None:
            logger.warning("Can not plot, no tf coils data found.")
            return
        text_labels = []
        shapes = []
        for _, coil_info in coils_dict.items():
            conductors = coil_info["conductors"]
            if hasattr(coil_info, "identifier"):
                name = coil_info["identifier"]
            else:
                name = coil_info["name"]

            cx = 0
            cy = 0
            for _, conductor_info in conductors.items():
                elements = conductor_info["elements"]
                if "outline" not in conductor_info:
                    # cross_sections = conductor_info["cross_section"]
                    scatter = ax.scatter(
                        elements["start_points"]["r"], elements["start_points"]["z"], color=color, s=10
                    )
                    shapes.append(scatter)
                    scatter = ax.scatter(elements["end_points"]["r"], elements["end_points"]["z"], color=color, s=10)
                    shapes.append(scatter)

                    for ielement in range(len(elements.types)):
                        if elements["types"][ielement] == 1:  # line

                            r1 = elements["start_points"]["r"][ielement]
                            z1 = elements["start_points"]["z"][ielement]
                            r2 = elements["end_points"]["r"][ielement]
                            z2 = elements["end_points"]["z"][ielement]
                            if ielement == 0:
                                cx = r1
                                cy = z1
                            segment = Polygon(
                                [[r1, z1], [r2, z2]], closed=False, edgecolor=color, facecolor="none", linewidth=1
                            )
                            ax.add_patch(segment)
                            shapes.append(segment)
                else:
                    # Plot cross-section contours if available
                    outline = conductor_info.get("outline", {})

                    # Convert to numpy arrays for easier manipulation
                    x1 = np.array(outline["inner"]["r"])
                    y1 = np.array(outline["inner"]["z"])
                    x2 = np.array(outline["outer"]["r"])
                    y2 = np.array(outline["outer"]["z"])

                    # Close the contour loops by appending the first point to the end
                    x1 = np.append(x1, x1[0])
                    y1 = np.append(y1, y1[0])
                    x2 = np.append(x2, x2[0])
                    y2 = np.append(y2, y2[0])

                    # Create filled polygon connecting inner and outer contours
                    x_fill = np.append(x1, x2[::-1])
                    y_fill = np.append(y1, y2[::-1])

                    # Plot contour lines
                    line1 = ax.plot(x1, y1, color=edgecolor, linewidth=1, alpha=alpha)
                    line2 = ax.plot(x2, y2, color=edgecolor, linewidth=1, alpha=alpha)
                    shapes.extend(line1)
                    shapes.extend(line2)

                    fill_patch = ax.fill(x_fill, y_fill, alpha=0.7, linewidth=0, facecolor=facecolor)
                    shapes.extend(fill_patch)

            name = ""
            if coil_info["identifier"]:
                name = coil_info["identifier"]
            elif coil_info["name"]:
                name = f"{coil_info['name']}"

            text = ax.text(cx, cy, name, fontsize="small", color="#333333", visible=False)
            text_labels.append(text)
        tf_legend = Patch(color=color, label="tf")

        ax.set_aspect("equal", adjustable="box")
        tf_legend.is_label_visible = False
        tf_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "tf" in legend.get_text():
                visible = not tf_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                tf_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, Patch) and legend.get_label() == "tf":
                visible = not tf_legend.is_shape_visible
                for scatter in shapes:
                    scatter.set_visible(visible)
                tf_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, tf")
        else:
            ax.set_title("tf")
        return tf_legend


def sectional_interpolation(x, y, points_per_section=20):
    """
    Apply adaptive interpolation to contour sections with smart
    gradient control for line segments.

    This function uses a two-pass approach:
    1. First pass: Identify all line segments in the contour
    2. Second pass: Apply appropriate interpolation method

    This ensures smooth transitions between line segments and curves.

    Parameters
    ----------
    x, y : array_like
        1D arrays of the polygon vertices, ordered along the loop.
    points_per_section : int, optional
        Number of points to interpolate in each section (default: 20).

    Returns
    -------
    xs, ys : ndarray
        Interpolated points along the smoothed contour.

    Notes
    -----
    Three interpolation strategies based on segment type:

    1. **Line segments** (both P1 and P2 on a line):
       - Uses linear interpolation: x = (1-t)*x1 + t*x2
       - Guarantees perfect straightness (zero deviation)

    2. **Curved sections** (both P1 and P2 on curves):
       - Uses cubic Hermite with Catmull-Rom gradients
       - g1 = 0.5 * (P2 - P0), g2 = 0.5 * (P3 - P1)
       - Provides smooth curve interpolation

    3. **Transitions** (one point on line, one on curve):
       - Uses cubic Hermite with mixed gradients
       - Line points use line segment gradient
       - Curve points use Catmull-Rom gradient
       - Ensures smooth transition between line and curve
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if len(x) < 4:
        return x, y

    # Ensure the contour is closed
    if not (x[0] == x[-1] and y[0] == y[-1]):
        x = np.append(x, x[0])
        y = np.append(y, y[0])

    # Remove duplicate closing point for processing
    x_open = x[:-1]
    y_open = y[:-1]
    n = len(x_open)

    # FIRST PASS: Identify all line segments
    # For each point, store whether it's part of a line segment
    is_on_line = np.zeros(n, dtype=bool)
    line_gradients = {}  # Store gradient for each point on a line

    for i in range(n):
        # Check triplet: P(i-1), P(i), P(i+1)
        im1 = (i - 1) % n
        ip1 = (i + 1) % n

        if _is_collinear(x_open[im1], y_open[im1], x_open[i], y_open[i], x_open[ip1], y_open[ip1]):
            is_on_line[i] = True
            # Store the line segment gradient at this point
            line_gradients[i] = (x_open[ip1] - x_open[i], y_open[ip1] - y_open[i])

    # SECOND PASS: Interpolate using computed gradients
    xs_new = []
    ys_new = []

    for i in range(n):
        # Get 4 consecutive points with wraparound
        p0_idx = i
        p1_idx = (i + 1) % n
        p2_idx = (i + 2) % n
        p3_idx = (i + 3) % n

        x0, y0 = x_open[p0_idx], y_open[p0_idx]
        x1, y1 = x_open[p1_idx], y_open[p1_idx]
        x2, y2 = x_open[p2_idx], y_open[p2_idx]
        x3, y3 = x_open[p3_idx], y_open[p3_idx]

        # Add the starting point of this section
        xs_new.append(x1)
        ys_new.append(y1)

        # Calculate gradients at P1 and P2 based on line membership
        if is_on_line[p1_idx]:
            # P1 is on a line - use the precomputed line gradient
            g1_x, g1_y = line_gradients[p1_idx]
        else:
            # P1 is on a curve - use Catmull-Rom gradient
            g1_x, g1_y = 0.5 * (x2 - x0), 0.5 * (y2 - y0)

        if is_on_line[p2_idx]:
            # P2 is on a line - use the precomputed line gradient
            g2_x, g2_y = line_gradients[p2_idx]
        else:
            # P2 is on a curve - use Catmull-Rom gradient
            g2_x, g2_y = 0.5 * (x3 - x1), 0.5 * (y3 - y1)

        # Check if both P1 and P2 are on a line segment
        if is_on_line[p1_idx] and is_on_line[p2_idx]:
            # Use linear interpolation for line segments
            for j in range(1, points_per_section):
                t = j / points_per_section
                x_interp = (1 - t) * x1 + t * x2
                y_interp = (1 - t) * y1 + t * y2
                xs_new.append(x_interp)
                ys_new.append(y_interp)
        else:
            # Apply cubic Hermite interpolation for curves or transitions
            for j in range(1, points_per_section):
                t = j / points_per_section
                t2 = t * t
                t3 = t2 * t

                # Hermite basis functions
                h1 = 2 * t3 - 3 * t2 + 1
                h2 = -2 * t3 + 3 * t2
                h3 = t3 - 2 * t2 + t
                h4 = t3 - t2

                x_interp = h1 * x1 + h2 * x2 + h3 * g1_x + h4 * g2_x
                y_interp = h1 * y1 + h2 * y2 + h3 * g1_y + h4 * g2_y

                xs_new.append(x_interp)
                ys_new.append(y_interp)

    # Close the contour
    xs_new.append(xs_new[0])
    ys_new.append(ys_new[0])

    return np.array(xs_new), np.array(ys_new)


def _is_collinear(x1, y1, x2, y2, x3, y3, tolerance=1e-6):
    """
    Check if three points are collinear (lie on the same straight line).

    Uses the cross product method: if the cross product of vectors
    (p1->p2) and (p2->p3) is zero, the points are collinear.

    Parameters
    ----------
    x1, y1, x2, y2, x3, y3 : float
        Coordinates of the three points to check.
    tolerance : float, optional
        Numerical tolerance for collinearity check (default: 1e-6).

    Returns
    -------
    bool
        True if the three points are collinear within tolerance.
    """
    # Calculate cross product of vectors (p1->p2) and (p2->p3)
    # Cross product = (x2-x1)*(y3-y2) - (y2-y1)*(x3-x2)
    cross_product = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)

    # Check if cross product is close to zero
    return abs(cross_product) < tolerance


def periodic_closed_spline(x, y, num=64, smooth=0.0, k=2):
    """
    Build a periodic spline through a closed 2D loop and resample it.

    Parameters
    ----------
    x, y : array_like
        1D arrays of the polygon vertices, ordered along the loop.
        They may include the first point again at the end; if so,
        the duplicate endpoint is removed automatically.
    num : int, optional
        Number of points to sample on the smooth curve (default: 400).
    smooth : float, optional
        Smoothing factor passed to splprep. 0 means interpolation
        (curve passes exactly through all input points). Larger values
        produce smoother curves that only approximate the points.
    k : int, optional
        Spline degree (1 to 5). Default is cubic (3).

    Returns
    -------
    xs, ys : ndarray
        Sampled points along the smooth periodic curve, length `num`.
    tck : tuple
        Spline representation as returned by splprep (useful if you
        want to evaluate derivatives, etc.).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape")

    if x.ndim != 1:
        raise ValueError("x and y must be one-dimensional")

    if x.size < k + 1:
        raise ValueError(f"Need at least k+1={k+1} points for a degree-{k} spline")

    # If the loop already repeats the first point at the end, drop the duplicate.
    if np.allclose([x[0], y[0]], [x[-1], y[-1]]):
        x = x[:-1]
        y = y[:-1]

    # Build a periodic parametric spline (x(u), y(u)), u in [0, 1]
    tck, u = splprep([x, y], s=smooth, per=True, k=k)

    # Sample along the spline
    u_new = np.linspace(0.0, 1.0, num)
    xs, ys = splev(u_new, tck)

    return np.asarray(xs), np.asarray(ys), tck

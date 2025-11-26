"""
This module provides compute functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging
import math

import numpy as np
from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger("module")


class TFCompute:
    """This class provides compute functions for tf ids"""

    def __init__(self, ids: object):
        """Initialization PfPassiveCompute object.

        Args:
            ids : tf ids object
        """
        self.ids = ids

    def get_tf_coils(self, select_coil=":", select_conductor=":") -> dict:
        """
        Retrieve information about the Toroidal Field (TF) coils and their conductors.

        Args:
            select_coil (str, optional): A string representing the selection of coils.
                         Defaults to ":" which selects all coils.
            select_conductor (str, optional): A string representing the selection of conductors.
                              Defaults to ":" which selects all conductors.

        Returns:
            dict: A dictionary containing information about the selected TF coils and their conductors.
                If no coils are found, a warning is logged and None is returned.
        """
        coil_arrays = list(self.ids.coil)
        if select_coil is not None:
            coil_arrays = get_slice_from_array(coil_arrays, select_coil)
        coils = {}
        for coil_index, coil in enumerate(coil_arrays):
            coil_info = {}
            if hasattr(coil, "identifier"):
                coil_info["identifier"] = coil.identifier
            else:
                coil_info["identifier"] = ""
            coil_info["name"] = coil.name
            coil_info["resistance"] = coil.resistance
            coil_info["turns"] = coil.turns
            conductor_arrays = list(coil.conductor)
            if select_conductor is not None:
                conductor_arrays = get_slice_from_array(conductor_arrays, select_conductor)
            conductors = {}
            for conductor_index, conductor in enumerate(conductor_arrays):
                conductor_info = {}
                conductor_info["elements"] = conductor.elements
                conductor_info["cross_section"] = conductor.cross_section
                # Add outline only for line segment elements with valid cross-section
                if np.all(conductor.elements.types == 1) and len(conductor.cross_section) == 1:
                    n = len(conductor.elements.start_points.r)
                    nskip = max(1, math.ceil(n / 180))
                    conductor_info["outline"] = get_outline(conductor, skip=nskip)
                conductors[conductor_index] = conductor_info

            coil_info["conductors"] = conductors
            coils[coil_index] = coil_info
        if not coils:
            logger.warning("tf.coil is empty")
            return None
        return coils


# ============================================================================
# Public API Functions
# ============================================================================


def get_outline(conductor, use_three_point_algorithm=True, skip=1):
    """
    Extract inner and outer contour coordinates for TF coil conductor cross-sections.

    This function computes the inner and outer boundary coordinates of a TF coil
    conductor by analyzing the cross-section geometry and applying the maximum
    normal offset from the conductor centerline. Two algorithms are available:
    1. Three-point algorithm: Uses middle points from three consecutive points
    2. Two-point algorithm: Uses interpolated centerline approach

    Parameters
    ----------
    conductor : object
        A conductor object containing elements and cross_section data from the
        IMAS TF coil data structure.
    use_three_point_algorithm : bool, optional
        If True (default), use three-point algorithm for non-collinear points.
        If False, use the original two-point interpolation algorithm.
    skip : int, optional
        Sampling rate for points. If skip=1 (default), use all points.
        If skip=10, use every 10th point for faster computation.
        Useful for visualization when high precision is not required.

    Returns
    -------
    dict
        A dictionary with the following structure:
        {
            'inner': {'r': list, 'z': list},
            'outer': {'r': list, 'z': list}
        }
        where:
        - 'inner' contains the inner boundary coordinates (R, Z)
        - 'outer' contains the outer boundary coordinates (R, Z)
        - Coordinates are computed based on selected algorithm

    Notes
    -----
    - Only processes elements with type 1 (line segment)
    - Only handles cross-sections with geometry_type == 1 (polygon outline)
    - Three-point algorithm: selects middle points of non-collinear triplets
    - Two-point algorithm: interpolates centerline then computes outlines
    - Uses the maximum normal coordinate to determine conductor thickness
    - Returns empty lists if no valid cross-section data is found
    - Higher skip values reduce computation time but lower outline resolution
    """
    elements = conductor.elements
    cross_section = conductor.cross_section

    # Initialize return dictionary
    outline_dict = {"inner": {"r": [], "z": []}, "outer": {"r": [], "z": []}}

    # Calculate coil center coordinates
    x_center = np.average(elements.start_points.r)
    y_center = np.average(elements.start_points.z)

    if use_three_point_algorithm:
        # Three-point algorithm: use middle points of non-collinear triplets
        return _get_outline_three_point(elements, cross_section, x_center, y_center, outline_dict, skip)
    else:
        # Original two-point interpolation algorithm
        return _get_outline_interpolation(elements, cross_section, x_center, y_center, outline_dict, skip)


# ============================================================================
# Coordinate Transformation Functions
# ============================================================================


def tn_to_xy(t, n, x_start, y_start, x_end, y_end, x_center, y_center):
    """
    Convert local (T, N) coordinates to Cartesian (x, y) for a general
    planar coil segment.

    The local frame is defined as:
      - T : unit tangent vector from (x_start, y_start) to (x_end, y_end)
      - N : unit normal vector, perpendicular to T, chosen so that it points
            more towards the coil center (x_center, y_center).

    That is, among the two possible normals ±N, we pick the one whose
    dot product with the vector from the reference point to the center is
    non-negative.

    Parameters
    ----------
    t, n : float or ndarray
        Local coordinates along T (tangent) and N (normal).
    x_start, y_start : float or ndarray
        Cartesian coordinates of the start point of the coil segment.
    x_end, y_end : float or ndarray
        Cartesian coordinates of the end point of the coil segment.
    x_center, y_center : float or ndarray
        Cartesian coordinates of (an approximate) coil center used to
        resolve the sign ambiguity of N.

    Returns
    -------
    x, y : float or ndarray
        Cartesian coordinates corresponding to the given (t, n) in the
        local (T, N) frame at the start point.

    Notes
    -----
    - T is always tangent to the segment from start to end.
    - N is perpendicular to T and chosen to point towards the center.
    - All inputs are converted to NumPy arrays and broadcast according
      to NumPy's broadcasting rules.
    - If the start and end points coincide, a ValueError is raised.
    - The local frame origin is at the start point.
    """

    # Convert to arrays for broadcasting
    t = np.asarray(t)
    n = np.asarray(n)
    x_start = np.asarray(x_start)
    y_start = np.asarray(y_start)
    x_end = np.asarray(x_end)
    y_end = np.asarray(y_end)
    x_center = np.asarray(x_center)
    y_center = np.asarray(y_center)

    # Determine reference point (always use start point)
    x_ref = x_start
    y_ref = y_start

    # Tangent direction T: from start to end
    dx = x_end - x_start
    dy = y_end - y_start
    seg_len = np.hypot(dx, dy)

    if np.any(seg_len == 0.0):
        raise ValueError("Start and end points coincide; tangent undefined.")

    Tx = dx / seg_len
    Ty = dy / seg_len

    # Two candidate normals, perpendicular to T
    # N1: rotate T by +90 degrees (CCW)
    Nx1 = -Ty
    Ny1 = Tx
    # N2 = -N1 would be the opposite side

    # Vector from reference point to center
    cx = x_center - x_ref
    cy = y_center - y_ref

    # Decide which normal points more towards the center
    # If dot((cx, cy), N1) >= 0, use N1; otherwise use -N1
    dot1 = cx * Nx1 + cy * Ny1
    use_N1 = dot1 >= 0

    Nx = np.where(use_N1, Nx1, -Nx1)
    Ny = np.where(use_N1, Ny1, -Ny1)

    # Map local (t, n) -> global (x, y) from reference point
    x = x_ref + t * Tx + n * Nx
    y = y_ref + t * Ty + n * Ny

    return x, y


def tn_to_xy_three_points(x1, y1, x2, y2, x3, y3, n, x_center, y_center):
    """
    Convert local (T, N) coordinates to Cartesian (x, y) for a coil segment
    defined by three points, where T is computed from 1st and 3rd points
    and the reference position is the 2nd (middle) point.

    Parameters
    ----------
    x1, y1 : float or ndarray
        Cartesian coordinates of the first point.
    x2, y2 : float or ndarray
        Cartesian coordinates of the second point (reference/middle point).
    x3, y3 : float or ndarray
        Cartesian coordinates of the third point.
    n : float or ndarray
        Normal coordinate (distance from centerline).
    x_center, y_center : float or ndarray
        Cartesian coordinates of (an approximate) coil center used to
        resolve the sign ambiguity of N.

    Returns
    -------
    x_offset, y_offset : float or ndarray
        Cartesian coordinates corresponding to the given normal offset
        from the middle point (x2, y2).

    Notes
    -----
    - T is computed as unit vector from point 1 to point 3
    - N is perpendicular to T and chosen to point towards the center
    - Reference point for coordinate transformation is the middle point
    - If points 1 and 3 coincide, a ValueError is raised
    """
    # Convert to arrays for broadcasting
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    x2 = np.asarray(x2)
    y2 = np.asarray(y2)
    x3 = np.asarray(x3)
    y3 = np.asarray(y3)
    n = np.asarray(n)
    x_center = np.asarray(x_center)
    y_center = np.asarray(y_center)

    # Tangent direction T: from point 1 to point 3
    dx = x3 - x1
    dy = y3 - y1
    seg_len = np.hypot(dx, dy)

    if np.any(seg_len == 0.0):
        raise ValueError("Points 1 and 3 coincide; tangent is undefined.")

    Tx = dx / seg_len
    Ty = dy / seg_len

    # Two candidate normals, perpendicular to T
    # N1: rotate T by +90 degrees (CCW)
    Nx1 = -Ty
    Ny1 = Tx

    # Vector from middle point (x2, y2) to center
    cx = x_center - x2
    cy = y_center - y2

    # Decide which normal points more towards the center
    # If dot((cx, cy), N1) >= 0, use N1; otherwise use -N1
    dot1 = cx * Nx1 + cy * Ny1
    use_N1 = dot1 >= 0

    Nx = np.where(use_N1, Nx1, -Nx1)
    Ny = np.where(use_N1, Ny1, -Ny1)

    # Map normal offset from middle point (x2, y2)
    x_offset = x2 + n * Nx
    y_offset = y2 + n * Ny

    return x_offset, y_offset


# ============================================================================
# Utility Functions
# ============================================================================


def are_points_collinear(x1, y1, x2, y2, x3, y3, tolerance=1e-9):
    """
    Check if three points are collinear (lie on the same line).

    Uses the cross product method: if the cross product of vectors
    (P2-P1) and (P3-P1) is close to zero, the points are collinear.

    Parameters
    ----------
    x1, y1 : float
        Coordinates of the first point.
    x2, y2 : float
        Coordinates of the second point.
    x3, y3 : float
        Coordinates of the third point.
    tolerance : float, optional
        Tolerance for considering points as collinear. Default is 1e-9.

    Returns
    -------
    bool
        True if the three points are collinear within the given tolerance,
        False otherwise.

    Notes
    -----
    - Uses cross product magnitude compared to tolerance
    - Accounts for the scale of the coordinates by normalizing
    """
    # Vectors from point 1 to points 2 and 3
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x3 - x1
    dy2 = y3 - y1

    # Cross product magnitude
    cross_product = abs(dx1 * dy2 - dy1 * dx2)

    # Scale tolerance by the magnitude of the vectors
    scale = max(abs(dx1), abs(dy1), abs(dx2), abs(dy2), 1.0)

    return cross_product < tolerance * scale


def _get_outline_three_point(elements, cross_section, x_center, y_center, outline_dict, skip=1):
    """
    Three-point algorithm for outline extraction.
    Selects middle points from non-collinear triplets.

    Parameters
    ----------
    skip : int, optional
        Sampling rate for points. If skip=1, use all points.
        If skip=10, use every 10th point.
    """
    # Collect all valid centerline points first
    centerline_points = []
    valid_cross_sections = []

    for ielement in range(len(elements.types)):
        # Skip points based on sampling rate
        if ielement % skip != 0:
            continue

        if elements.types[ielement] == 1:  # line segment
            if len(cross_section) == 1:
                cs_index = 0
            elif len(cross_section) > 1:
                cs_index = ielement
            else:
                continue

            cs = cross_section[cs_index]
            centerline_points.append((elements.start_points.r[ielement], elements.start_points.z[ielement]))
            valid_cross_sections.append(cs)

    if len(centerline_points) < 3:
        return outline_dict

    # Get thickness information from first cross-section
    cs = valid_cross_sections[0]
    if cs.geometry_type.index == 1:  # polygon outline
        n_inner = np.max(cs.outline.normal)
        n_outer = np.min(cs.outline.normal)
    else:
        n_inner = abs(cs.width / 2.0)
        n_outer = -n_inner

    inner_r_points = []
    inner_z_points = []
    outer_r_points = []
    outer_z_points = []

    # Process triplets of consecutive points (including wraparound for closed loop)
    # Phase 1: Process all collinear triplets first
    processed_points = set()  # Track which points have been processed

    for i in range(len(centerline_points)):
        # Handle wraparound indices for closed loop geometry
        prev_idx = (i - 1) % len(centerline_points)
        curr_idx = i
        next_idx = (i + 1) % len(centerline_points)

        x1, y1 = centerline_points[prev_idx]  # previous point
        x2, y2 = centerline_points[curr_idx]  # current point (middle)
        x3, y3 = centerline_points[next_idx]  # next point

        # Check if points are collinear
        if are_points_collinear(x1, y1, x2, y2, x3, y3, tolerance=1e-6):
            # Points are collinear, add inner/outer points for all three points
            # For collinear points, use tangent direction from first to third

            # Add points for first point (x1, y1)
            xi1, yi1 = tn_to_xy(0.0, n_inner, x1, y1, x3, y3, x_center, y_center)
            xo1, yo1 = tn_to_xy(0.0, n_outer, x1, y1, x3, y3, x_center, y_center)
            inner_r_points.append(xi1)
            inner_z_points.append(yi1)
            outer_r_points.append(xo1)
            outer_z_points.append(yo1)

            # Add points for middle point (x2, y2)
            # Calculate the position parameter t for the middle point
            xi2, yi2 = tn_to_xy(0.0, n_inner, x2, y2, x3, y3, x_center, y_center)
            xo2, yo2 = tn_to_xy(0.0, n_outer, x2, y2, x3, y3, x_center, y_center)
            inner_r_points.append(xi2)
            inner_z_points.append(yi2)
            outer_r_points.append(xo2)
            outer_z_points.append(yo2)

            # Add points for third point (x3, y3)
            xi3, yi3 = tn_to_xy(0.0, n_inner, x3, y3, x1, y1, x_center, y_center)
            xo3, yo3 = tn_to_xy(0.0, n_outer, x3, y3, x1, y1, x_center, y_center)
            inner_r_points.append(xi3)
            inner_z_points.append(yi3)
            outer_r_points.append(xo3)
            outer_z_points.append(yo3)

            # Mark all three points as processed
            processed_points.add(prev_idx)
            processed_points.add(curr_idx)
            processed_points.add(next_idx)

    # Phase 2: Process non-collinear triplets, skipping already processed points
    for i in range(len(centerline_points)):
        # Skip if current point was already processed in Phase 1
        if i in processed_points:
            continue

        # Handle wraparound indices for closed loop geometry
        prev_idx = (i - 1) % len(centerline_points)
        curr_idx = i
        next_idx = (i + 1) % len(centerline_points)

        x1, y1 = centerline_points[prev_idx]  # previous point
        x2, y2 = centerline_points[curr_idx]  # current point (middle)
        x3, y3 = centerline_points[next_idx]  # next point

        # Check if points are collinear (should be false since we processed collinear ones first)
        if not are_points_collinear(x1, y1, x2, y2, x3, y3, tolerance=1e-6):
            # Points are not collinear, use three-point algorithm
            xi, yi = tn_to_xy_three_points(x1, y1, x2, y2, x3, y3, n_inner, x_center, y_center)
            xo, yo = tn_to_xy_three_points(x1, y1, x2, y2, x3, y3, n_outer, x_center, y_center)

            inner_r_points.append(xi)
            inner_z_points.append(yi)
            outer_r_points.append(xo)
            outer_z_points.append(yo)

    # Sort and remove duplicates for inner and outer contours
    inner_r_sorted, inner_z_sorted = _sort_and_deduplicate_contour(inner_r_points, inner_z_points)
    outer_r_sorted, outer_z_sorted = _sort_and_deduplicate_contour(outer_r_points, outer_z_points)

    # Store the results
    outline_dict["inner"]["r"] = inner_r_sorted
    outline_dict["inner"]["z"] = inner_z_sorted
    outline_dict["outer"]["r"] = outer_r_sorted
    outline_dict["outer"]["z"] = outer_z_sorted

    return outline_dict


def _get_outline_interpolation(elements, cross_section, x_center, y_center, outline_dict, skip=1):
    """
    Original interpolation algorithm for outline extraction.

    Parameters
    ----------
    skip : int, optional
        Sampling rate for points. If skip=1, use all points.
        If skip=10, use every 10th point.
    """
    # Collect centerline points for interpolation
    start_r_points = []
    start_z_points = []
    end_r_points = []
    end_z_points = []
    valid_cross_sections = []

    # First pass: collect all valid centerline points
    for ielement in range(len(elements.types)):
        # Skip points based on sampling rate
        if ielement % skip != 0:
            continue

        if elements.types[ielement] == 1:  # line segment
            if len(cross_section) == 1:
                cs_index = 0
            elif len(cross_section) > 1:
                cs_index = ielement
            else:
                continue

            cs = cross_section[cs_index]
            if cs.geometry_type.index == 1:  # polygon outline
                # Collect centerline points
                start_r_points.append(elements.start_points.r[ielement])
                start_z_points.append(elements.start_points.z[ielement])
                end_r_points.append(elements.end_points.r[ielement])
                end_z_points.append(elements.end_points.z[ielement])
                valid_cross_sections.append(cs)

    if len(start_r_points) == 0:
        return outline_dict

    # Convert to numpy arrays
    start_r_points = np.array(start_r_points)
    start_z_points = np.array(start_z_points)
    end_r_points = np.array(end_r_points)
    end_z_points = np.array(end_z_points)

    # Use the original centerline points without interpolation
    start_r_interp = start_r_points
    start_z_interp = start_z_points
    end_r_interp = end_r_points
    end_z_interp = end_z_points

    # Initialize arrays to collect outline points
    inner_r_points = []
    inner_z_points = []
    outer_r_points = []
    outer_z_points = []

    # Compute outlines from interpolated centerline
    # Use the first cross-section for thickness information
    cs = valid_cross_sections[0]
    n_inner = np.max(cs.outline.normal)
    n_outer = np.min(cs.outline.normal)

    for i in range(len(start_r_interp)):
        x_start = start_r_interp[i]
        y_start = start_z_interp[i]
        x_end = end_r_interp[i]
        y_end = end_z_interp[i]
        t = 0.0

        xi, yi = tn_to_xy(t, n_inner, x_start, y_start, x_end, y_end, x_center, y_center)

        xo, yo = tn_to_xy(t, n_outer, x_start, y_start, x_end, y_end, x_center, y_center)

        inner_r_points.append(xi)
        inner_z_points.append(yi)
        outer_r_points.append(xo)
        outer_z_points.append(yo)

    # Store the results
    outline_dict["inner"]["r"] = inner_r_points
    outline_dict["inner"]["z"] = inner_z_points
    outline_dict["outer"]["r"] = outer_r_points
    outline_dict["outer"]["z"] = outer_z_points

    return outline_dict


def _sort_and_deduplicate_contour(r_points, z_points, tolerance=1e-9):
    """
    Sort contour points in counter-clockwise order and remove duplicates.

    This function takes a list of R, Z coordinates, removes duplicate points
    within tolerance, and sorts the remaining points in counter-clockwise
    order around their centroid.

    Parameters
    ----------
    r_points : list or ndarray
        R-coordinates of the contour points.
    z_points : list or ndarray
        Z-coordinates of the contour points.
    tolerance : float, optional
        Distance tolerance for considering points as duplicates.
        Default is 1e-9.

    Returns
    -------
    r_sorted : list
        R-coordinates sorted in counter-clockwise order with duplicates removed.
    z_sorted : list
        Z-coordinates sorted in counter-clockwise order with duplicates removed.

    Notes
    -----
    - Uses centroid as reference point for angular sorting
    - Counter-clockwise ordering is based on angle from centroid
    - Duplicate points within tolerance are removed (keeps first occurrence)
    - Returns empty lists if no valid points remain after processing
    """
    if len(r_points) == 0:
        return [], []

    # Convert to numpy arrays
    r_points = np.array(r_points)
    z_points = np.array(z_points)

    # Remove duplicates within tolerance
    unique_r = []
    unique_z = []

    for i, (r, z) in enumerate(zip(r_points, z_points)):
        # Check if this point is too close to any existing unique point
        is_duplicate = False
        for ur, uz in zip(unique_r, unique_z):
            distance = np.sqrt((r - ur) ** 2 + (z - uz) ** 2)
            if distance < tolerance:
                is_duplicate = True
                break

        # Only add the point if it's not a duplicate
        if not is_duplicate:
            unique_r.append(r)
            unique_z.append(z)

    if len(unique_r) == 0:
        return [], []

    # Calculate centroid
    centroid_r = np.mean(unique_r)
    centroid_z = np.mean(unique_z)

    # Calculate angles from centroid to each point
    angles = []
    for r, z in zip(unique_r, unique_z):
        angle = np.arctan2(z - centroid_z, r - centroid_r)
        angles.append(angle)

    # Sort points by angle (counter-clockwise order)
    sorted_indices = np.argsort(angles)

    r_sorted = [unique_r[i] for i in sorted_indices]
    z_sorted = [unique_z[i] for i in sorted_indices]

    return r_sorted, z_sorted

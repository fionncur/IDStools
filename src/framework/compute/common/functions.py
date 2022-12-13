"""
This is a common module which has common functions which can be used across ll IDSes

"""
import numpy as np


def get_nearest_value_in_array(
    time_array: np.ndarray, time_of_interest: float
) -> tuple:
    """Element in nd array `a` closest to the scalar value `a0`

    Args:
        time_array (np.ndarray, ): [description]
        time_of_interest ([float]): [description]

    Returns:
        [np.ndarray]: [time value]
        [float]: [nearest time index]
    """
    time_index = abs(time_array - time_of_interest).argmin()
    return time_index, time_array.flat[time_index]


def compute_time_index(time_array: np.ndarray, time_of_interest: float) -> tuple:
    """
    Get time index of time of interste

    Args:
        time_array ([np.ndarray]): [numpy array]
        time_of_interest ([float]): [time requested]

    Returns:
        [int]: [integer index found for time requested]
        [float]: [nearest time for time requested]
    """
    time_value = 0
    time_index = 0
    time_len = len(time_array)
    # length of time array is 1
    if time_len == 1:
        time_value = time_array[0]
        return time_index, time_array[0]

    # length of array is bigger than 1 and asking for valid time of interest
    if time_of_interest >= 0:
        time_index, time_value = get_nearest_value_in_array(
            time_array, time_of_interest
        )
        return time_index, time_value

    # time of interest is not valid then calculate default
    time_index = int(time_len / 2)
    time_value = time_array[time_index]
    return time_index, time_value

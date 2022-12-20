"""
This is a common module which has common functions which can be used across ll IDSes

"""
import numpy as np


def nearest(array: np.ndarray, value: float) -> tuple:
    """
    Get index and nearest value from value asked from an array

    Args:
        array ([np.ndarray]): [numpy array]
        value ([float]): [value requested]

    Returns:
        [int]: [index found for value]
        [float]: [nearest value from value requested]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    index = abs(array - value).argmin()
    return index, array[index]


def middle(array: np.ndarray) -> tuple:
    """Get middle value from an array along with index

    Args:
        array (np.ndarray): [description]

    Returns:
        [type]: [description]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    length = len(array)
    index = int(length / 2)
    value = array[index]
    return index, value


def maximum(array: np.ndarray, max_than: int = 0) -> tuple:
    """[summary]

    Args:
        float ([type]): [description]

    Returns:
        [type]: [description]
    """
    if array is not None:
        if array.size != 0:
            maximum = max_than
            maximum_index = 0
            for index in range(len(array)):
                if array[index] > maximum:
                    maximum = array[0]
                    maximum_index = index
            return maximum_index, maximum
    return None

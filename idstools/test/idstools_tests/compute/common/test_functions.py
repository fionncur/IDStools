"""
Test common compute functions
"""

import numpy as np

from idstools.compute.common import (
    get_closest_of_given_value_from_array,
    get_middle_element_from_array,
)

array = [
    0.21069679,
    0.61290182,
    0.63425412,
    0.84635244,
    0.91599191,
    0.00213826,
    0.17104965,
    0.56874386,
    0.57319379,
    0.28719469,
]
full_array = np.asarray(array)
single_array = np.asarray([0.21069679])
empty_array = np.asarray([])


def test_get_closest_of_given_value_from_array():
    """
    test nearest function
    """
    index, value = get_closest_of_given_value_from_array(full_array, value=0.5)
    assert value == 0.56874386, "nearest function is not producing correct result"

    index, value = get_closest_of_given_value_from_array(single_array, value=0.5)
    assert value == 0.21069679, "nearest function is not producing correct result"

    value = get_closest_of_given_value_from_array(empty_array, value=0.5)
    assert value is None, "nearest function is not producing correct result"

    index, value = get_closest_of_given_value_from_array(full_array, value=-20)
    assert value == 0.00213826, "nearest function is not producing correct result"


def test_get_middle_element_from_array():
    """
    test middle function
    """

    index, value = get_middle_element_from_array(full_array)
    assert value == 0.00213826, "middle function is not producing correct result"

    index, value = get_middle_element_from_array(single_array)
    assert value == 0.21069679, "middle function is not producing correct result"

    value = get_middle_element_from_array(empty_array)
    assert value is None, "middle function is not producing correct result"

"""
Test common compute functions
"""
import os
import sys

import numpy as np
import pytest

from idstools.compute.common.basic import getClosestOfGivenValueFromArray, getMiddleElementFromArray

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


def test_getClosestOfGivenValueFromArray():
    """
    test nearest function
    """
    index, value = getClosestOfGivenValueFromArray(full_array, value=0.5)
    assert value == 0.56874386, "nearest function is not producing correct result"

    index, value = getClosestOfGivenValueFromArray(single_array, value=0.5)
    assert value == 0.21069679, "nearest function is not producing correct result"

    value = getClosestOfGivenValueFromArray(empty_array, value=0.5)
    assert value == None, "nearest function is not producing correct result"

    index, value = getClosestOfGivenValueFromArray(full_array, value=-20)
    assert value == 0.00213826, "nearest function is not producing correct result"


def test_getMiddleElementFromArray():
    """
    test middle function
    """

    index, value = getMiddleElementFromArray(full_array)
    assert value == 0.00213826, "middle function is not producing correct result"

    index, value = getMiddleElementFromArray(single_array)
    assert value == 0.21069679, "middle function is not producing correct result"

    value = getMiddleElementFromArray(empty_array)
    assert value == None, "middle function is not producing correct result"

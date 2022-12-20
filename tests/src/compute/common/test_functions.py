"""
Test common compute functions
"""
import numpy as np
import os
import pytest
import sys

root_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)

sys.path.append(root_path)

from src.compute.common.functions import middle, nearest

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


def test_nearest():
    """
    test nearest function
    """
    index, value = nearest(full_array, value=0.5)
    assert value == 0.56874386, "nearest function is not producing correct result"

    index, value = nearest(single_array, value=0.5)
    assert value == 0.21069679, "nearest function is not producing correct result"

    value = nearest(empty_array, value=0.5)
    assert value == None, "nearest function is not producing correct result"

    index, value = nearest(full_array, value=-20)
    assert value == 0.00213826, "nearest function is not producing correct result"


def test_middle_full():
    """
    test middle function
    """

    index, value = middle(full_array)
    assert value == 0.00213826, "middle function is not producing correct result"

    index, value = middle(single_array)
    assert value == 0.21069679, "middle function is not producing correct result"

    value = middle(empty_array)
    assert value == None, "middle function is not producing correct result"

import os
import numpy as np
from turtle import circle
import pytest
from PySTL.core import stl_to_array, array_to_stl
from PySTL.shapes import Circle


@pytest.fixture()
def make_result_dir(scope="session"):
    if os.path.exists(os.path.join(os.getcwd(), 'Results')):
        pass
    else:
        os.mkdir("Results")
    return os.path.join(os.getcwd(), 'Results')


@pytest.fixture
def make_circle(make_result_dir):
    circle = Circle()
    circle.create()
    filename = os.path.join(make_result_dir, 'circle.stl')
    circle.export(filename, 'circle')
    return os.path.join(make_result_dir, "circle.stl")


@pytest.fixture
def make_circle_array(make_circle):
    if os.path.exists(make_circle):
        art = stl_to_array(make_circle)
        return art


def test_stl_to_array(make_circle):
    """Tests if the converted file is a numpy array."""
    art = stl_to_array(stl=make_circle)
    assert isinstance(art, np.ndarray) == True


def test_array_to_stl(make_circle_array):
    array_to_stl(make_circle_array, "Results/array_to_stl")
    assert os.path.exists(os.path.join(
        os.getcwd(), "Results", "array_to_stl.stl")) == True

import os
from turtle import circle
import pytest
from PySTL.core import stl_to_array
from PySTL.shapes import Circle


@pytest.fixture()
def make_result_dir(scope="session"):
    if os.path.exists(os.path.join(os.getcwd(), 'Results')):
        pass
    else:
        os.mkdir("Results")
    return os.path.join(os.getcwd(), 'Results')


def test_stl_to_array(make_result_dir):
    circle = Circle()
    circle.create()
    filename = os.path.join(make_result_dir, 'circle.stl')
    circle.export(filename, 'circle')
    assert os.path.exists(os.path.join(make_result_dir, "circle.stl"))

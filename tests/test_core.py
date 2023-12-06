from fnmatch import translate
import os
from matplotlib.pylab import rand
import numpy as np
import pytest
from pistl.core import stl_to_array, array_to_stl, translate, rotate
from pistl.shapes import Circle


@pytest.fixture()
def make_result_dir(scope="session"):
    """Creates the directory for test files and does not get rid of it
    It should be torn down."""
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
    """Test if array is converted to stl."""
    array_to_stl(make_circle_array, "Results/array_to_stl")
    assert os.path.exists(os.path.join(
        os.getcwd(), "Results", "array_to_stl.stl")) == True


def test_translate():
    """Picks random points in the circle stl before and after and checks if translation
    happened by correct amount.
    WARNING: created a deep copy because the translate method chnages the original array."""
    art = stl_to_array(stl='Results/circle.stl')
    art_copy = art.copy()
    trans_art = translate(arr=art, x_offset=1.00, y_offset=2.00, z_offset=1.00)
    random_point = np.random.randint(1, trans_art.shape[0])
    # checks translation in y
    assert np.abs(art_copy[1:][random_point, 1] -
                  trans_art[random_point, 1]) == 2
    # checks translation in x
    assert np.abs(art_copy[1:][random_point, 0] -
                  trans_art[random_point, 0]) == 1
    # checks translation in z
    assert np.abs(art_copy[1:][random_point, 2] -
                  trans_art[random_point, 2]) == 1

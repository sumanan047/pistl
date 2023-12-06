import pytest
import os
import numpy as np
from pistl.utilities import find_normal, stl_writer

# creating an asset for the test and need to tear it down.


@pytest.fixture
def make_result_dir(scope="session"):
    if os.path.exists(os.path.join(os.getcwd(), 'Results')):
        pass
    else:
        os.mkdir("Results")
    return os.path.join(os.getcwd(), 'Results')


def test_find_nromal():
    """Tests the normal finding function in simplest case."""
    nn = find_normal([0, 1, 0], [0, 4, 0], [0, 2, 50])
    arr1 = np.array([1.0, 0.0, 0.0])
    assert np.allclose(arr1, nn) == True


def test_write_stl_new_file(make_result_dir):
    """Test the stl file writing function."""
    filename = os.path.join(make_result_dir, 'new_stl.stl')
    stl_writer(filename, 'tetra', [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                   [[1, 0, 0], [0, 1, 0], [0, 0, 0]]],
               facet_normals=[[0.57, 0.57, 0.57],
                              [0, 0, -1]])
    assert os.path.isfile(filename) == True


def test_write_stl(make_result_dir):
    """Test if the written file is at correct place."""
    path = os.path.join(make_result_dir, "new_stl.stl")
    assert os.path.isfile(path) == True

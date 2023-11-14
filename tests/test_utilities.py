import os
import numpy as np
from PySTL.utilities import find_normal, stl_writer

# creating an asset for the test and need to tear it down.
os.mkdir("Results")

def test_find_nromal():
    """Tests the normal finding function in simplest case."""
    nn = find_normal([0,1,0],[0,4,0],[0,2,50])
    arr1 = np.array([1.0,0.0,0.0])
    assert  np.allclose(arr1, nn) == True

def test_write_stl_new_file():
    """Test the stl file writing function."""
    path = os.path.join(os.getcwd(), 'Results')
    filename = os.path.join(path, 'new_stl.stl')
    stl_writer(filename,'tetra', [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                    [[1, 0, 0], [0, 1, 0], [0, 0, 0]]], 
                                    facet_normals=[[0.57,0.57,0.57],
                                                    [0,0,-1]])
    assert os.path.isfile(filename) == True

def test_write_stl():
    """Test if the written file is at correct place."""
    path = os.path.join(os.getcwd(), "Results","new_stl.stl")
    assert os.path.isfile(path) == True
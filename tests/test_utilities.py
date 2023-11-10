import os
import numpy as np
from PySTL.utilities import find_normal, stl_writer


def test_find_nromal():
    nn = find_normal([0,1,0],[0,4,0],[0,2,50])
    arr1 = np.array([1.0,0.0,0.0])
    assert  np.allclose(arr1, nn) == True

def test_write_stl_new_file():
    "Only checks if the file exists!"
    stl_writer(r'.\Results\new_stl.stl','tetra', [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                    [[1, 0, 0], [0, 1, 0], [0, 0, 0]]], 
                                    facet_normals=[[0.57,0.57,0.57],
                                                    [0,0,-1]])
    assert os.path.isfile(r'.\Results\new_stl.stl') == True

def test_write_stl():
    "Checks is written!"
    assert os.path.isfile(r'.\Results\test.stl') == True
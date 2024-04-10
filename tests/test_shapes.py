from pistl import shapes
from pistl import pist_exceptions
import pytest


def test_shapes_init():
    """Tests the base class initiation."""
    s = shapes.Shape()
    assert s.x is None
    assert s.y is None
    assert s.name == ""
    assert s.mode == None
    assert s.filename is None
    assert s.shapename is None


def test_shapes_create():
    """Tests baseclass does not create any shape other than None."""
    s = shapes.Shape()
    assert s.create() is None


def test_visualize():
    s = shapes.Shape()
    with pytest.raises(pist_exceptions.Visualization_Exceptions):
        s.visualize()


def test_export():
    s = shapes.Shape()
    s.create()
    s.export("Hello", "Hi")
    assert s.filename == "Hello"
    assert s.shapename == "Hi"


def test_shape_creation():
    shape_list = [shapes.Circle(),
                  shapes.Cylinder(),
                  shapes.Pyramid(),
                  shapes.Sphere(),
                  shapes.Tetrahedron()]
    for s in shape_list:
        s.create()
        s.export("Results/shape.stl", "shape")
        s.visualize()

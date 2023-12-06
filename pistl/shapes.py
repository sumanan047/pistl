# native python
import os
# dependecies
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
# internal custom imports
from . import utilities
"""
Module Content:
1. Shape
2. Circle
3. Cylinder
4. Cuboid
5. Tetrahedron
6. Pyramid
7. Sphere : Create Octahedron, hexagon etc using special cases of the spheres.
"""


class Shape(object):
    """Base class for shapes.Provides a generic init and three methods
    to create, visualize and export the shapes."""

    def __init__(self) -> None:
        self.x = None
        self.y = None
        self.z = None
        self.name = ""
        self.mode = None

    def create(self):
        """Should be overwritten by child class depending on how to prodcuce that shape."""
        return None

    def visualize(self):
        """Plots the shape in desired backend."""

    def export(self):
        """Exports the shape in desired format."""
        return None

    @staticmethod
    def _write_triangles_and_normals(triangle_list: list, normal_list: list, p1: list, p2: list, p3: list):
        """
        Description:
            Takes in a scheme of three points and adds to a list of triangles and normals in the stl.
        Paremters:
            triangle_list: list of triangles in the stl.
            normal_list: list of normals of the traingles in the stl
            p1, p2 and p3 are list objects that are three points on a triangle."""
        triangle_list.append([p1, p2, p3])
        normal_list.append(list(utilities.find_normal(p1, p2, p3)))
        return None


class Circle(Shape):
    """
    Description:
        Creates a 2D circle. 
        Special cases can be used to generate rectangle and triangles.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "Circle"
        self._center = [0.0, 0.0]
        self._radius = 1.0
        self.dim = 2.0
        self._area = np.pi*(np.power(self._radius, 2))
        self._perimeter = 2*np.pi*self._radius
        self.resolution = 10

    @property
    def radius(self):
        return self._radius

    @property
    def perimeter(self):
        return 2*np.pi*self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def area(self):
        return np.pi*(np.power(self._radius, 2))

    def create(self, elevation=0.0):
        """
        Description:
            Creates a circle with a constant z value.
        Parmeters:
            elevation: The z value or elevation of the circle. Default value is 0.0.
        Example:
        >>> circle = Cicrle()
        >>> circle.create() # creates a circle of elevation of 0.0
        >>> circle.create(elevation=10.0) # creates the circle at z = 10.0
        """
        theta = np.linspace(0, 2*np.pi, self.resolution)
        self.x = self._radius*np.cos(theta) + self._center[0]
        self.y = self._radius*np.sin(theta) + self._center[1]
        self.z = [elevation]*len(self.x)
        return None

    def visualize(self):
        """Plots the circle using one of the provided backends."""
        if self.mode is None:
            fig, ax = plt.subplots(1, 1)
            ax.set_xlim(-2*self._radius, 2*self._radius)
            ax.set_ylim(-2*self._radius, 2*self._radius)
            ax.set_xlabel('x-axis')
            ax.set_ylabel('y-axis')
            ax.set_title(f'{self.name}')
            return ax
        elif self.mode == "pv":
            mesh = pv.read("Results/circle.stl")
            return mesh

    def export(self, filename: str, shapename: str):
        """
        Description:
            Takes x and y cordinates from the circle function and generates a cricle stl of
            desired resolution that has 0 elevation i.e. all z values are zero.
        Parameters:
            filename: string filename of the .stl file
            shapename: name of the object that is created
        Example:
        >>> circle=Cirle()
        >>> circle.radius = 2.0
        >>> circle.create()
        >>> circle.visualize()
        >>> circle.export('circle.stl', circle)
        """
        triangle_list = []
        normal_list = []
        assert (len(self.x) == len(self.y)
                ), "length of x and y should be same, found different."
        for i in range(len(self.x)-1):
            p1 = [0, 0, self.z[i]]
            p2 = [self.x[i], self.y[i], self.z[i]]
            p3 = [self.x[i+1], self.y[i+1], self.z[i]]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        utilities.stl_writer(filename, shapename, triangle_list, normal_list)
        return None


class Cylinder(Shape):
    """Generates a cylinder for a height along the z-axis."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "Cylinder"
        self._base_circle_radius = 1.00
        self._base_circle_center = [0.0, 0.0, 0.0]
        self._height = 1.00
        self._top_circle_radius = self._base_circle_radius
        self._top_circle_center = [
            self._base_circle_center[0], self._base_circle_center[1], self._height]
        self._cylinder_center = [self._base_circle_center[0] +
                                 self._height/2, self._base_circle_center[1]+self._height/2]
        self.dim = 3.0
        self.resolution = 10
        self.close = False

    def create(self):
        """
        Description:
            Creates a cylinder.
        Parmeters:
            None
        Example:
        >>> cyl = Cylinder()
        >>> cyl._height = 10.00
        >>> cyl._top_circle_radius = 4.00
        >>> cyl._base_circle_radius = 4.00
        >>> cyl.resolution = 10
        >>> cyl.close = True
        >>> cyl.create()
        """
        # create the base circle
        self.theta = np.linspace(0, 2*np.pi, self.resolution)
        self.base_x = self._base_circle_radius * \
            np.cos(self.theta) + self._base_circle_center[0]
        self.base_y = self._base_circle_radius * \
            np.sin(self.theta) + self._base_circle_center[1]
        self.base_z = len(self.base_x)*self._base_circle_center[2]
        # create the top circle
        self.top_x = self._top_circle_radius * \
            np.cos(self.theta) + self._top_circle_center[0]
        self.top_y = self._top_circle_radius * \
            np.sin(self.theta) + self._top_circle_center[1]
        self.top_z = len(self.top_x)*self._top_circle_center[2]
        return None

    def visualize(self):
        """Visualize the cylinder using a backend of choice."""
        if self.mode is None:
            # plot setting
            f1 = plt.figure()
            ax = f1.add_subplot(1, 1, 1, projection=Axes3D.name)
            ax.view_init(elev=20, azim=35, roll=10)
            # create a 2D grid for cordinates in surface plots
            z = np.linspace(0, self._height, self.resolution)
            theta = np.linspace(0, 2*np.pi, self.resolution)
            theta_grid, z_grid = np.meshgrid(theta, z)
            assert (self._base_circle_radius ==
                    self._top_circle_radius), "Right now frustums cannot be visualized."
            x_grid = self._base_circle_radius * \
                np.cos(theta_grid) + self._base_circle_center[0]
            y_grid = self._base_circle_radius * \
                np.sin(theta_grid) + self._base_circle_center[1]
            return ax.plot_surface(x_grid, y_grid, z_grid)
        elif self.mode == "pv":
            mesh = pv.read('Results/cyl.stl')
            return mesh

    def export(self, filename, shapename):
        """
        Description:
            Takes x and y cordinates from the two circles one at top and the other at bottom face 
            connects them using triangles. Finally, closes the top and bottom face of the cylinder
            if the close attribute on the shape is True.
        Parameters:
            filename: string filename of the .stl file
            shapename: name of the object that is created
        """
        triangle_list = []
        normal_list = []
        assert (len(self.base_x) == len(self.base_y)
                ), "length of x and y should be same, found different."
        # first set of triangles
        for i in range(len(self.base_x)-1):
            p1 = [self.base_x[i], self.base_y[i], self.base_z]
            p2 = [self.top_x[i+1], self.top_y[i+1], self.top_z]
            p3 = [self.top_x[i], self.top_y[i], self.top_z]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        # second set of triangles
        for i in range(len(self.base_x)-1):
            p1 = [self.base_x[i], self.base_y[i], self.base_z]
            p2 = [self.base_x[i+1], self.base_y[i+1], self.base_z]
            p3 = [self.top_x[i+1], self.top_y[i+1], self.top_z]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        if self.close == True:
            # close top face
            for i in range(len(self.top_x)-1):
                p1 = [0, 0, self.top_z]
                p2 = [self.top_x[i], self.top_y[i], self.top_z]
                p3 = [self.top_x[i+1], self.top_y[i+1], self.top_z]
                self._write_triangles_and_normals(
                    triangle_list, normal_list, p1, p2, p3)
            # close bottom face
            for i in range(len(self.base_x)-1):
                p1 = [0, 0, self.base_z]
                p2 = [self.base_x[i+1], self.base_y[i+1], self.base_z]
                p3 = [self.base_x[i], self.base_y[i], self.base_z]
                self._write_triangles_and_normals(
                    triangle_list, normal_list, p1, p2, p3)
        utilities.stl_writer(filename, shapename, triangle_list, normal_list)
        return None


class Cuboid(Cylinder):
    """Generates a cuboid using special case of a cylinder with changed parameters."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._side_length = 1.00
        self.resolution = 5
        self.close = False

    def _set_side(self):
        """Sets the side of the cuboid because inheriting from cylinder only sets the radius."""
        self._base_circle_radius = self._side_length/(np.sqrt(2))
        self._top_circle_radius = self._side_length/(np.sqrt(2))
        return None

    def _set_resolution(self):
        """Sets resolution to call cylinder class and make a cuboid."""
        self.resolution = 5
        return None

    def create(self):
        """Inherits a cylinder and sets sides and resolution to create a cuboid."""
        self._set_side()
        self._set_resolution()
        return super().create()

    def visualize(self, mode=None):
        return super().visualize()

    def export(self, filename, shapename):
        return super().export(filename, shapename)


class Tetrahedron(Circle):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resolution = 4
        self.close = True

    def create(self, elevation=-2.0):
        """Creates a tetrahedron with base elevation i.e. z"""
        return super().create(elevation)

    def visualize(self):
        return super().visualize()

    def export(self, filename, shapename):
        """
        Description:
            Creates a tetrahedron from a circle class by chnaging the base circle
            shape and elavtion on of the center.
        Parameters:
            filename: string filename of the .stl file
            shapename: name of the object that is created."""
        triangle_list = []
        normal_list = []
        assert (len(self.x) == len(self.y)
                ), "length of x and y should be same, found different."
        for i in range(len(self.x)-1):
            p1 = [0, 0, 0]
            p2 = [self.x[i], self.y[i], self.z[i]]
            p3 = [self.x[i+1], self.y[i+1], self.z[i]]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        utilities.stl_writer(filename, shapename, triangle_list, normal_list)
        return None


class Pyramid(Tetrahedron):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.resolution = 5
        self.close = False

    def create(self, elevation=-2):
        return super().create(elevation)

    def visualize(self):
        return super().visualize()

    def export(self, filename, shapename):
        """
        Description:
            Creates a pyramid from a circle class by chnaging the base circle
            shape and elavtion on of the center.
        Parameters:
            filename: string filename of the .stl file
            shapename: name of the object that is created."""
        triangle_list = []
        normal_list = []
        assert (len(self.x) == len(self.y)
                ), "Length of x and y should be same, found different."
        # the dome loop
        for i in range(len(self.x)-1):
            p1 = [0, 0, 0]
            p2 = [self.x[i], self.y[i], self.z[i]]
            p3 = [self.x[i+1], self.y[i+1], self.z[i]]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        # close the base
        if self.close == True:
            p1 = [self.x[0], self.y[0], self.z[0]]
            p2 = [self.x[1], self.y[1], self.z[1]]
            p3 = [self.x[2], self.y[2], self.z[2]]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
            p1 = [self.x[0], self.y[0], self.z[0]]
            p2 = [self.x[-1], self.y[-1], self.z[-1]]
            p3 = [self.x[-2], self.y[-2], self.z[-2]]
            self._write_triangles_and_normals(
                triangle_list, normal_list, p1, p2, p3)
        utilities.stl_writer(filename, shapename, triangle_list, normal_list)
        return None


class Sphere(Shape):
    def __init__(self) -> None:
        super().__init__()
        self.center = [0, 0, 0]
        self.radius = 1.0
        self.resoultion_longitude = 20
        self.resolution_latitude = 20
        self.name = "Sphere"

    def _radius_variation(self, min_radius):
        """
        Description:
            Internal method that sets the radius of the latitudes in the sphere.
        Parameters:
            min_radius:
                Minimum radius of the circle on top of the sphere."""
        self.radius_list = []
        lin_space = np.linspace(self.radius, min_radius,
                                int(self.resoultion_longitude/2))
        for l in lin_space:
            temp_rad = np.sqrt(np.power(self.radius, 2) - np.power(l, 2))
            self.radius_list.append(temp_rad)
        lin_space = np.linspace(min_radius, self.radius,
                                int(self.resoultion_longitude/2))
        for l in lin_space:
            temp_rad = np.sqrt(np.power(self.radius, 2) - np.power(l, 2))
            self.radius_list.append(temp_rad)

    def create(self, min_radius: float = 0.1):
        """
        Description:
            Creates the required circles of latitudes for the spheres.
        Parameters:
            min_radius:
                Minimum radius of the circle on top of the sphere."""
        self.circle_list = []
        self.latitude = np.linspace(-self.radius/1.0,
                                    self.radius/1.0, self.resoultion_longitude)
        self._radius_variation(min_radius=min_radius)
        for i, l in enumerate(self.latitude):
            circle = Circle()
            circle.radius = self.radius_list[i]
            circle.resolution = self.resolution_latitude
            # it looks like 1.0 but the elevation is actually l as in L.
            circle.create(elevation=l)
            self.circle_list.append(circle)
        return None

    def visualize(self):
        """Loads the stl to visualize in pyvista."""
        mesh = pv.read('Results/sphere.stl')
        return mesh

    def export(self, filename, shapename):
        """
        Creates a stack of circles.
        """
        triangle_list = []
        normal_list = []
        # creates stack of disks
        for j in range(len(self.circle_list)-1):
            circle_1 = self.circle_list[j]
            circle_2 = self.circle_list[j+1]
            # first set of triangle
            #  i x> i+1                  > circle 2
            #  x   x
            #  i x                       > circle 1
            for i in range(len(circle_1.x)-1):
                p1 = [circle_1.x[i], circle_1.y[i], circle_1.z[i]]
                p2 = [circle_2.x[i+1], circle_2.y[i+1], circle_2.z[i+1]]
                p3 = [circle_2.x[i], circle_2.y[i], circle_2.z[i]]
                self._write_triangles_and_normals(
                    triangle_list, normal_list, p1, p2, p3)
            # add next set of triangles
            #  i x                       > circle 2
            #  x   x
            #  i x> i+1                  > circle 1
            for i in range(len(circle_1.x)-1):
                p1 = [circle_1.x[i], circle_1.y[i], circle_1.z[i]]
                p2 = [circle_1.x[i+1], circle_1.y[i+1], circle_1.z[i+1]]
                p3 = [circle_2.x[i+1], circle_2.y[i+1], circle_2.z[i+1]]
                self._write_triangles_and_normals(
                    triangle_list, normal_list, p1, p2, p3)
        # close the top
        end_circle = [self.circle_list[0], self.circle_list[-1]]
        for i in range(len(end_circle)):
            cur_circle = end_circle[i]
            for j in range(len(cur_circle.x)-1):
                p1 = [0, 0, cur_circle.z[j]]
                p2 = [cur_circle.x[j], cur_circle.y[j], cur_circle.z[j]]
                p3 = [cur_circle.x[j+1], cur_circle.y[j+1], cur_circle.z[j+1]]
                self._write_triangles_and_normals(
                    triangle_list, normal_list, p1, p2, p3)
        utilities.stl_writer(filename, shapename, triangle_list, normal_list)
        return None


if __name__ == "__main__":
    if os.path.isdir("Results"):
        os.chdir(os.path.join(os.getcwd(), "Results"))
    else:
        os.mkdir("Results")
        os.chdir(os.path.join(os.getcwd(), "Results"))
    utilities.stl_writer('test.stl', 'tetra', [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                               [[1, 0, 0], [0, 1, 0], [0, 0, 0]]],
                         facet_normals=[[0.57, 0.57, 0.57],
                                        [0, 0, -1]])
    # circle test
    circle = Circle()
    circle.radius = 2.0
    circle.create()
    circle.visualize()
    circle.export('circle.stl', 'circle')

    # cylinder test
    cyl = Cylinder()
    cyl._height = 10.00
    cyl._top_circle_radius = 4.00
    cyl._base_circle_radius = 4.00
    cyl.resolution = 20
    cyl.close = True
    cyl.create()
    cyl.visualize()
    cyl.export('cyl.stl', 'cyl')

    # cuboid test
    cub = Cuboid()
    cub._height = 10.00
    cub._side_length = 1.0
    cub.close = True
    cub.create()
    cub.visualize()
    cub.export('cub.stl', 'cub')

    # tetra example
    tetra = Tetrahedron()
    tetra.close = True
    tetra.create(elevation=-2.00)  # set a height instead of this
    tetra.visualize()
    tetra.export('tetra.stl', 'tetra')

    # pyramid example
    pyramid = Pyramid()
    pyramid.resolution = 5
    pyramid.close = True
    pyramid.create()
    pyramid.visualize()
    pyramid.export('pyramid.stl', 'pyramid')

    # sphere example
    sphere = Sphere()
    sphere.create()
    sphere.visualize()
    sphere.export('sphere.stl', 'sphere')

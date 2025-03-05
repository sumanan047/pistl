import numpy as np
from . import utilities
"""
### Core module contains funcitions that can be used to translate, 
twist and deform the stl shapes

array structure:
np.array([normal, v1, v2, v3])..keep concatenating next triangles
The shape should be:
    (4* number of triangles, 3)
"""


def stl_to_array(stl: str):
    """
    Description:
        Reads an stl file produced by pystl and converts that into a compact numpy array of the form:
        np.array([0,0,0], [normla, vertex..], ....all the triangles).
        The shape of the array then produced is:
            4* number of traingles + 1 (first element is [0,0,0] in the array made for vstack to work.)
    Parameters:
        stl:
            string filehandle for the shape.
    Returns:
        a numpy array of the shape described in the description section of the docstring.
    Example:
        >>> art = stl_to_array(stl='Results/stl_name_before_translate.stl')
        >>> print(type(art))
        <class numpy.ndarray>
    """
    stl_array = np.array([0, 0, 0], dtype=float)
    with open(stl, 'r') as f:
        for line in f:
            if ('normal' or 'vertex' in line):
                line = line.rstrip('\n')
                strip_list = line.split(' ')[-3:]
                if len(strip_list) >= 3:  # and 'object' not in strip_list:
                    try:
                        arr = [float(l) for l in strip_list]
                    except:
                        arr = [0.0 for l in strip_list]
                    stl_array = np.vstack((stl_array, arr))
    return stl_array


def array_to_stl(arr: np.ndarray, stl_name: str):
    """
    Description:
        Takes an array and writes the corresponding stl file using the infomormation on normal and vertices
        of triangles in the array.
    Parameter:
        arr: an array of shape:
            4*n + 1, 3
        stl_name:
            Name of the stl file that is to be created.
    Returns:
        None
    """
    if arr.shape[0] % 4 == 0.00:
        arr = arr
    else:
        arr = arr[1:]
    with open(f"{stl_name}.stl", "w") as f:
        f.write(f"solid stl_name\n")
        for i in range(int(arr.shape[0]/4)):
            f.write(
                f"facet normal {float(arr[4*i][0])} {float(arr[4*i][1])} {float(arr[4*i][2])}\n")
            f.write('outer loop\n')
            f.write(
                f"vertex {float(arr[4*i+1][0])} {float(arr[4*i+1][1])} {float(arr[4*i+1][2])}\n")
            f.write(
                f"vertex {float(arr[4*i+2][0])} {float(arr[4*i+2][1])} {float(arr[4*i+2][2])}\n")
            f.write(
                f"vertex {float(arr[4*i+3][0])} {float(arr[4*i+3][1])} {float(arr[4*i+3][2])}\n")
            f.write('endloop\n')
            f.write('endfacet\n')
            # print(arr[i,:])
        f.write("endsolid")
    return None


def translate(arr: np.ndarray, x_offset: float = 0.00, y_offset: float = 0.00, z_offset: float = 0.00):
    """
    Description:
        Takes a stl array and translates it by a provided x_offset, y_offset and z_offset.
    Parameters:
        arr:
            stl array that is translated
        x_offset:
            required distance along x-axis by which the stl has to be moved.
        y_offset:
            required distance along y-axis by which the stl has to be moved.
        z_offset:
            required distance along z-axis by which the stl has to be moved.
    Returns:
        translated stl array
    """
    if arr.shape[0] % 4 == 0.00:
        arr = arr
    else:
        arr = arr[1:]
    for i in range(int(arr.shape[0]/4)):
        arr[4*i+1][0] = float(arr[4*i+1][0]) + x_offset
        arr[4*i+2][0] = float(arr[4*i+2][0]) + x_offset
        arr[4*i+3][0] = float(arr[4*i+3][0]) + x_offset
        # translate y
        arr[4*i+1][1] = float(arr[4*i+1][1]) + y_offset
        arr[4*i+2][1] = float(arr[4*i+2][1]) + y_offset
        arr[4*i+3][1] = float(arr[4*i+3][1]) + y_offset
        # translate z
        arr[4*i+1][2] = float(arr[4*i+1][2]) + z_offset
        arr[4*i+2][2] = float(arr[4*i+2][2]) + z_offset
        arr[4*i+3][2] = float(arr[4*i+3][2]) + z_offset
    return arr


def rotate(arr: np.ndarray,
           x_theta: float = 0.00,
           y_theta: float = 0.00,
           z_theta: float = 0.00,
           filename='rotated.stl'):
    """
    Description:
        Rotates the stl file around the angles x_theta, y_theta and z_theta.
        where x_theta is the rotation around x-axis or rotation in y-z plane and likewise.
    Parameters:
        arr: 
            The stl array to be rotated
        x_theta:
            in yz plane or around x-axis
        y_theta:
            in xz plane or around y-axis
        z_theta:
            in xy plane or around z-axis
    Returns:
        Rotated stl array.
    """
    x_theta = np.radians(x_theta)
    y_theta = np.radians(y_theta)
    z_theta = np.radians(z_theta)
    # Create a rotation matrix around the x-axis
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(x_theta), -np.sin(x_theta)],
        [0, np.sin(x_theta), np.cos(x_theta)]
    ])

    # Create a rotation matrix around the y-axis
    R_y = np.array([
        [np.cos(y_theta), 0, np.sin(y_theta)],
        [0, 1, 0],
        [-np.sin(y_theta), 0, np.cos(y_theta)]
    ])

    # Create a rotation matrix around the z-axis
    R_z = np.array([
        [np.cos(z_theta), -np.sin(z_theta), 0],
        [np.sin(z_theta), np.cos(z_theta), 0],
        [0, 0, 1]
    ])
    BigR = np.dot(R_x, np.dot(R_y, R_z))
    if arr.shape[0] % 4 == 0.00:
        arr = arr
    else:
        arr = arr[1:]
    rotated_triangles = []
    normals = []
    for i in range(int(arr.shape[0]/4)):
        point_1 = np.array([arr[4*i+1][0], arr[4*i+1][1], arr[4*i+1][2]])
        point_2 = np.array([arr[4*i+2][0], arr[4*i+2][1], arr[4*i+2][2]])
        point_3 = np.array([arr[4*i+3][0], arr[4*i+3][1], arr[4*i+3][2]])
        rotated_point_1 = np.dot(BigR, point_1)
        rotated_point_2 = np.dot(BigR, point_2)
        rotated_point_3 = np.dot(BigR, point_3)
        rotated_triangles.append(
            [rotated_point_1, rotated_point_2, rotated_point_3])
        n = utilities.find_normal(
            rotated_point_1, rotated_point_2, rotated_point_3)
        normals.append(n)
    utilities.stl_writer(f"{filename}",
                         f'{filename}', rotated_triangles, normals)
    return None
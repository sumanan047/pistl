import numpy as np
# stl writer


def stl_writer(filename: str, stl_name: str, triangles: list, facet_normals: list = []):
    """
    Description:
        Generates a stl file provided the triangles and normal to the face.
    Parameters:
        filename - name of file to write to
        stl_anme
        facet_normals - num_triangles x 3 list of triangle normals
        triangles - List of triangles i.e. [T1, T2, T3],
                    where, Ti is a trinagle that is a list of three points: [[p0], [p1], [p2]], 
                    where, pi is a list of cordinates [x, y, z]
                    or see below:
                    num_triangles x 3 x 3 nested list: [ [ [p0], [p1], [p2] ] ... [ [p0], [p1], [p2] ] ]
    Returns:
        .stl file

    Example:
        >>> stl_writer('test.stl','tetra', [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                    [[1, 0, 0], [0, 1, 0], [0, 0, 0]]], 
                                    facet_normals=[[0.57,0.57,0.57],
                                                    [0,0,-1]])
    """
    with open(filename, 'w') as f:
        f.write(f'solid {stl_name}')
        for i in range(0, len(triangles)):
            f.write("\n")
            f.write(
                f"facet normal {facet_normals[i][0]} {facet_normals[i][1]} {facet_normals[i][2]}\n")
            f.write("outer loop\n")
            for v in triangles[i]:
                f.write("vertex {v1} {v2} {v3}\n".format(
                    v1=v[0], v2=v[1], v3=v[2]))
            f.write("endloop\n")
            f.write("endfacet\n")
        f.write("endsolid")


def find_normal(p1: list, p2: list, p3: list):
    """
    Description:
        Finds the normal of a triangle given three points.
    Parameters:
        p1: The first point of the triangle.
        p2: The second point of the triangle.
        p3: The third point of the triangle.
    Returns:
        A numpy array that is the normal for the triangle
        formed by the three points provided as the argument to the
        fucntion.
    Example:
        >>> p1 = [0,0,1]; p2 = [0,1,0]; p3 = [1,1,0]
        >>> n = find_normal()
        >>> n
        np.array([1,0,0])
    """
    # needs numpy array for the cross product to work
    pp1 = np.array(p1)
    pp2 = np.array(p2)
    pp3 = np.array(p3)
    # Calculate the cross product of the vectors from p1 to p2 and p1 to p3.
    n = np.cross(pp2 - pp1, pp3 - pp1)
    # TODO: very very bad exception handling
    try:
        # Normalize the vector.
        n = n / np.linalg.norm(n)
    except:
        n = np.array([0, 0, 0])
    return n

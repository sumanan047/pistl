# <h1 style="text-align:center; color:'red'">PISTL (pronounced as "Pistol")</h1>

<p text-align="center"><img src=".\assets\pystl_readme_cover.PNG" alt="Pystl_cover_image"></p>

<u>About the figure above</u>: Multiple shapes generated using PISTL as STL file and visualized in **Meshmixer** for the purpose of this picture. The visualization in PISTL can be done using pyvista, which is installed as a dependency.\_

### What is PISTL?

PISTL is a small (micro) library that can be used in python to programatically create stereolithographic (stl) files of regular geometric shapes like circle, cylinder, tetrahedron, sphere, pyramid and others by morphing these shapes. pystl also provide functions that can be used to translate and rotate these stl objects.

In summary:
PISTL can be used for the following purposes:

- to create simple geometric shape files in .stl format.
- visualize this stl files. [PySTL uses pyvista for such visualizations].
- perform simple transformations like translate, rotate and scale shapes.

### Examples

```python
# This example creates a sphere stl using pistl

# step 1.0: import PySTL
import pistl
from pistl import shapes

#instantiate a sphere shape
sphere = shapes.Sphere()

# set the radius of the sphere
sphere.radius = 10

# set resolution of the sphere in longitude and latitude
sphere.resolution_latitude = 200
sphere.resoultion_longitude = 200

# once you have set the radius and resolution, call create method
sphere.create()

# call export method to set stl filename and shape name
sphere.export('Results/sphere.stl', 'sphere')

# Finally visualize the shape in trame window or in a jupyter kernal using the visualize method.
sphere.visualize().plot(color='magenta', text=f'{sphere.name}')
```

<p text-align="center"><img src=".\assets\sphere.png" alt="Pystl_generated_sphere_stl"></p>

<u>PISTL is an open source project that welcomes contributions from developers from diverse community and backgrounds.\_</u>

contact : sumanan047@gmail.com to get added on the project formally.

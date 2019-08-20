import vtk
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def polydata_to_list(polydata):
    pts_nbr = polydata.GetNumberOfPoints()
    ret = []
    x = [] 
    y = []
    z = []
    
    for i in range(pts_nbr):
        ret.append(polydata.GetPoint(i))
        x.append(polydata.GetPoint(i)[0])
        y.append(polydata.GetPoint(i)[1])
        z.append(polydata.GetPoint(i)[2])
    return x, y, z

def do_read_stl_file(file_name):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_name)
    reader.Update()

    return reader.GetOutput()

def do_save_pts(pts):
    filename = 'guidewire.csv'
    with open(filename,'w') as fileobject:
        string_data = ''
        for pt in pts:
            string_data += str(pt[0]) + ';' + str(pt[1]) + ';' + str(pt[2]) + '\n'
        fileobject.write(string_data)
    fileobject.close


polydata = do_read_stl_file('C:\\Users\\cheng\\Desktop\\centerline.stl')
x,y,z = polydata_to_list(polydata)

#do_save_pts(pts)
fig2 = plt.figure(2)
ax3d = fig2.add_subplot(111, projection='3d')
ax3d.plot(x, y, z, 'bo')
#ax3d.plot(x_sample, y_sample, z_sample, 'r*')

plt.show()

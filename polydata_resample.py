import vtk

reader = vtk.vtkPolyDataReader()
reader.SetFileName(r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\liver.vtk")
reader.Update()

# print("number of raw points: ", reader.GetOutput().GetNumberOfPoints())

bound = reader.GetOutput().GetBounds()
print(bound)

sample = vtk.vtkPolyDataPointSampler()
sample.SetInputConnection(reader.GetOutputPort())
sample.SetDistance((bound[1]-bound[0])/100)
sample.Update()

source = vtk.vtkSphereSource()
source.SetRadius((bound[1]-bound[0]) * 0.01 * .75);

g3d = vtk.vtkGlyph3D()
g3d.SetInputConnection(sample.GetOutputPort())
g3d.SetSourceConnection(source.GetOutputPort())
g3d.ScalingOff()
g3d.Update()


# print("number of resampled points: ", sample.GetOutput().GetNumberOfPoints())

# Setup actor and mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(g3d.GetOutput())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

renderWindow = vtk.vtkRenderWindow()
renderWindow.SetWindowName("Line")
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderWindow.Render()
renderWindowInteractor.Start()

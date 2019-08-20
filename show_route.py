import vtk
import numpy as np
from route_plan import *


def lines_to_actors(points_array):
    """
    :param points_array: shape: [N+1, 3], line_array[0]为target point
    :return: N条从target point射出的射线
    """
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    for point in points_array:
        points.InsertNextPoint(point)

    # Create a cell array to store the lines in and add the lines to it
    lines = vtk.vtkCellArray()
    for i in range(1, points_array.shape[0]):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, i)
        lines.InsertNextCell(line)

    # Create a polydata to store everything in
    linesPolyData = vtk.vtkPolyData()

    # Add the points to the dataset         几何结构
    linesPolyData.SetPoints(points)

    # Add the lines to the dataset          拓扑结构
    linesPolyData.SetLines(lines)

    # Setup actor and mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetLineWidth(1)
    actor.GetProperty().SetColor([1.0, 1.0, 0.0])

    return actor


def vtk_to_actors(vtk_list):
    actors = []
    for file, prop in vtk_list.items():
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(file)
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(prop[:3])
        actor.GetProperty().SetOpacity(prop[3])
        actor.SetMapper(mapper)

        actors.append(actor)

    return actors


def show_organs_lines(organs_actors, line_actor):
    renderer = vtk.vtkRenderer()
    for actor in organs_actors:
        renderer.AddActor(actor)

    renderer.AddActor(line_actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Line")
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == "__main__":
    vtk_list = {r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\artery.vtk": [1.0, 0.0, 0.0, 0.9],
                r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\bone.vtk": [1.0, 1.0, 1.0, 1.0],
                r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\portalvein.vtk": [1.0, 0.0, 0.0, 0.8],
                r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\venoussystem.vtk": [1.0, 0.0, 0.0, 0.8],
                r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\liver.vtk": [0.5, 0.7, 0.7, .0],
                r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\livertumor03.vtk": [0.0, 1.0, 0.0, 1.0]}
    organs_actors = vtk_to_actors(vtk_list)

    # points_array = np.array([[0.0, 0.0, 0.0], [0.0, 100.0, 0.0], [0.0, .0, 100.0]])
    seed_point = getSeedPoint([r"D:\Annotation\3Dircadb1\3Dircadb1.8\MESHES_VTK\livertumor03.vtk"])
    print("seed point: " + str(seed_point))
    neg_array = polydatas2Array(readPolydatas(list(vtk_list.keys())[:-2]))

    points_array = routePlan(seed_point, neg_array, gap=36)
    line_actor = lines_to_actors(points_array)

    show_organs_lines(organs_actors, line_actor)

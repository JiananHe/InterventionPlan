import vtk
import numpy as np


def getSeedPoint(pos_files):
    pos_array = polydatas2Array(readPolydatas(pos_files))
    return np.mean(pos_array, axis=0)


def readPolydatas(file_list):
    polydata_list = []
    for file in file_list:
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(file)
        reader.Update()
        polydata_list.append(reader.GetOutput())

    return polydata_list


def resamplePolyData(polydata_list):
    resample_list = []
    for poly in polydata_list:
        bound = poly.GetBounds()
        print(bound)

        sample = vtk.vtkPolyDataPointSampler()
        sample.SetInputData(poly)
        sample.SetDistance(1)
        sample.Update()

        resample_list.append(sample.GetOutput())

    return resample_list


def polydatas2Array(polydata_list):
    arr = []
    for polydata in polydata_list:
        pts_nbr = polydata.GetNumberOfPoints()

        for i in range(pts_nbr):
            arr.append([polydata.GetPoint(i)[0], polydata.GetPoint(i)[1], polydata.GetPoint(i)[2]])

    return np.array(arr)


def polydatas2Actors(polydata_list, prop_list):
    actors = []
    for poly, prop in zip(polydata_list, prop_list):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)

        actor = vtk.vtkActor()
        actor.GetProperty().SetColor(prop[:3])
        actor.GetProperty().SetOpacity(prop[3])
        actor.SetMapper(mapper)

        actors.append(actor)

    return actors



import vtk
import numpy as np


def getTargetPoint(pos_files):
    """
    从肿瘤的vtk文件中获取其重心转为target point
    :param pos_files: 肿瘤的vtk文件
    :return: target point
    """
    pos_array = polydata2Array(readPolydatas(pos_files)[0])
    return np.mean(pos_array, axis=0)


def readPolydatas(file_list):
    """
    读取vtk文件
    :param file_list: vtk文件列表
    :return: 每个文件对应的polydata
    """
    polydata_list = []
    for file in file_list:
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(file)
        reader.Update()
        polydata_list.append(reader.GetOutput())

    return polydata_list


def polydata2Array(polydata):
    """
    获取polydata中的点的坐标
    :param polydata: polydata
    :return: 点的坐标，shape[N, 3]
    """
    arr = []
    pts_nbr = polydata.GetNumberOfPoints()

    for i in range(pts_nbr):
        arr.append([polydata.GetPoint(i)[0], polydata.GetPoint(i)[1], polydata.GetPoint(i)[2]])

    return np.array(arr)


def polydatas2Actors(polydata_list, prop_list):
    """
    为vtkPolyData构建vtkActor
    :param polydata_list: vtkPolyData列表，每个元素为一个vtkPolyData
    :param prop_list: 可视化属性，[R, G, B, Opacity]
    :return: vtkActor列表
    """
    assert len(polydata_list) == len(prop_list)
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



import vtk
import numpy as np


def routePlan(target_point, neg_polys, gap=1, line_len=300, angle=[0, 180]):
    """
    规划直线介入路径，路径为从target_point发出的射线；
    以target_point为原点建立球坐标系：射线与Y正轴夹角为beta，射线在X0Z平面的投影与X正轴夹角为alpha
    :param target_point: target point, shape: [1, 3]
    :param neg_polys: 需要避开的器官的polydata
    :param gap: 射线采样间隔(alpha与beta使用同样的间隔)
    :param line_len: 可视化的射线的长度
    :param angle: beta角度范围，即与y正轴的角度的范围
    :return: points_array，shape[M+1, 3]；points_array[0]为target_point, points_array[1:]为所有可取射线的起点坐标
    """

    # step1: 求出所有可能的射线，间隔为gap
    # 所有可能的射线集合α:[0, 360) * β:angle
    all_alpha_beta = np.array([[i, j] for i in range(0, 360, gap) for j in range(angle[0], angle[1] + 1, gap)])

    # 根据射线的alpha与beta，求出射线上距离target point为line_len长度的点的坐标
    all_alpha_beta = all_alpha_beta.astype(np.float64)
    all_alpha_beta *= (np.pi / 180)
    all_point_coords = np.array([line_len * np.sin(all_alpha_beta[:, 1]) * np.sin(all_alpha_beta[:, 0]),
                             line_len * np.cos(all_alpha_beta[:, 1]),
                             line_len * np.sin(all_alpha_beta[:, 1]) * np.cos(all_alpha_beta[:, 0])]).swapaxes(0, 1)

    all_point_coords = all_point_coords + target_point
    print("possible lines: ", all_point_coords.shape)
    set_point_coords = set(map(tuple, all_point_coords))

    # step2: 过滤射线，即判断每条射线是否与neg_polys存在交点
    for poly in neg_polys:
        obbTree = vtk.vtkOBBTree()
        obbTree.SetDataSet(poly)
        obbTree.BuildLocator()

        set_temp = set_point_coords.copy()
        for point in set_point_coords:
            f = obbTree.IntersectWithLine(target_point, list(point), None, None)
            if f != 0:  # the line insect with poly
                set_temp.remove(point)
        set_point_coords = set_temp.copy()

    # set to array
    pos_point_coords = np.array([np.array(t) for t in set_point_coords])
    print("positive lines: ", pos_point_coords.shape)

    return np.concatenate((np.array([target_point]), pos_point_coords))

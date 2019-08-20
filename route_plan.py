import vtk
import numpy as np


def routePlan(seed_point, neg_array, gap=1, line_len=300, angle=[0, 180]):
    """
    Planning ray intervention path
    :param seed_point: target point of rays, shape: [1, 3]
    :param neg_array: points through which a ray cannot pass, shape: [N, 3]
    :param gap: angle interval of rays
    :param line_len: the length of rays
    :param angle: beta角度范围，即与y正轴的角度的范围
    :return: alpha_beta: all available ray in spherical coordinate, shape: [M, 2],

    """
    # 直角坐标系转换F，使得target point为原点
    neg_array = neg_array - seed_point

    # 所有可能的射线集合α:[0, 360) * β:angle
    all_alpha_beta = np.array([[i, j] for i in range(0, 360, gap) for j in range(angle[0], angle[1] + 1, gap)])
    print("all possible line", all_alpha_beta.shape)

    # 求出所有不可取射线的α[0, 360)与β[0, 180]
    neg_alpha_beta = np.array([np.arctan(neg_array[:, 0] / neg_array[:, 2]),
                               np.arctan(np.sqrt(neg_array[:, 0] ** 2 + neg_array[:, 2] ** 2) /
                                         neg_array[:, 1])]).swapaxes(0, 1)
    neg_alpha_beta[neg_alpha_beta < 0] += np.pi
    neg_alpha_beta[:, 0][neg_array[:, 0] < 0] += np.pi
    neg_alpha_beta *= (180 / np.pi)
    print("all neg line: ", neg_alpha_beta.shape)

    # 过滤得到所有可取的射线
    set_alpha_beta = set(map(tuple, all_alpha_beta))
    for a in range(-gap, gap+1, gap):
        for b in range(-gap, gap+1, gap):
            neg_ff = np.concatenate((np.floor(neg_alpha_beta[:, 0])+a,
                                     np.floor(neg_alpha_beta[:, 1])+b)).reshape((-1, 2), order='F')
            neg_fc = np.concatenate((np.floor(neg_alpha_beta[:, 0])+a,
                                     np.ceil(neg_alpha_beta[:, 1])+b)).reshape((-1, 2), order='F')
            neg_cf = np.concatenate((np.ceil(neg_alpha_beta[:, 0])+a,
                                     np.floor(neg_alpha_beta[:, 1])+b)).reshape((-1, 2), order='F')
            neg_cc = np.concatenate((np.ceil(neg_alpha_beta[:, 0])+a,
                                     np.ceil(neg_alpha_beta[:, 1])+b)).reshape((-1, 2), order='F')
            set_alpha_beta = set_alpha_beta.difference(map(tuple, neg_ff))
            set_alpha_beta = set_alpha_beta.difference(map(tuple, neg_fc))
            set_alpha_beta = set_alpha_beta.difference(map(tuple, neg_cf))
            set_alpha_beta = set_alpha_beta.difference(map(tuple, neg_cc))

    # set to array
    pos_alpha_beta = np.array([np.array(t) for t in set_alpha_beta])
    print("all pos line: ", pos_alpha_beta.shape)

    # 根据射线的alpha与beta，求出射线上距离target point为line_len长度的点的坐标
    pos_alpha_beta = pos_alpha_beta.astype(np.float64)
    pos_alpha_beta *= (np.pi / 180)
    point_coords = np.array([line_len * np.sin(pos_alpha_beta[:, 1]) * np.sin(pos_alpha_beta[:, 0]),
                             line_len * np.cos(pos_alpha_beta[:, 1]),
                             line_len * np.sin(pos_alpha_beta[:, 1]) * np.cos(pos_alpha_beta[:, 0])]).swapaxes(0, 1)

    # 直角坐标系转换F'
    point_coords = point_coords + seed_point

    return np.concatenate((np.array([seed_point]), point_coords))

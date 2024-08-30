import os
import numpy as np

def process_single_file(file_path, save_dir, average_abs_x_target=0.006000193767249584, average_abs_y_target=0.01485129352658987):
    """
    处理单个 .npy 文件，并保存缩放后的结果
    :param file_path: str, 输入文件路径
    :param save_dir: str, 保存缩放后结果的目录
    :param average_abs_x_target: float, 目标 x 方向上的绝对值平均值
    :param average_abs_y_target: float, 目标 y 方向上的绝对值平均值
    :return: None
    """
    # 加载数据
    tangent_vectors = np.load(file_path, allow_pickle=True)

    # 检查数据的维度
    if tangent_vectors.ndim == 2:  # 处理二维数据
        tangent_vectors = np.expand_dims(tangent_vectors, axis=0)
    elif tangent_vectors.ndim != 3:
        print(f"Unexpected number of dimensions: {tangent_vectors.ndim}")
        return

    # 初始化 new_tangent_vectors
    new_tangent_vectors = np.zeros(tangent_vectors.shape)
    new_tangent_vectors = new_tangent_vectors.squeeze()

    # 确定行走方向
    sum_abs_x1 = np.abs(tangent_vectors[0, :10, 0]).sum()
    sum_abs_y1 = np.abs(tangent_vectors[0, :10, 1]).sum()
    sum_x1 = tangent_vectors[0, :10, 0].sum()
    sum_y1 = tangent_vectors[0, :10, 1].sum()

    tangent_vectors[:, :, 0] = tangent_vectors[:, :, 0] if sum_x1 > 0 else -tangent_vectors[:, :, 0]
    tangent_vectors[:, :, 1] = tangent_vectors[:, :, 1] if sum_y1 > 0 else -tangent_vectors[:, :, 1]

    if sum_abs_x1 < sum_abs_y1:  # y1是z+方向
        new_tangent_vectors[:, 1] = tangent_vectors[:, :, 1]
        new_tangent_vectors[:, 0] = tangent_vectors[:, :, 0]
    else:
        new_tangent_vectors[:, 0] = tangent_vectors[:, :, 1]
        new_tangent_vectors[:, 1] = tangent_vectors[:, :, 0]

    # 计算当前 x 和 y 方向的绝对值平均值
    average_abs_x_current = np.mean(np.abs(new_tangent_vectors[:, 0]))
    average_abs_y_current = np.mean(np.abs(new_tangent_vectors[:, 1]))

    # 计算缩放因子
    scale_x = average_abs_x_target / average_abs_x_current
    scale_y = average_abs_y_target / average_abs_y_current

    # 对 new_tangent_vectors 进行缩放
    new_tangent_vectors[:, 0] *= scale_x
    new_tangent_vectors[:, 1] *= scale_y

    # 保存缩放后的 new_tangent_vectors
    os.makedirs(save_dir, exist_ok=True)
    save_file_name = os.path.basename(file_path).replace('.npy', '_scaled.npy')
    save_path = os.path.join(save_dir, save_file_name)
    np.save(save_path, new_tangent_vectors)
    print(f"Saved scaled data to {save_path}")

def process_all_files(input_dir, save_dir, average_abs_x_target=0.006000193767249584, average_abs_y_target=0.01485129352658987):
    """
    批量处理目录下的所有 .npy 文件
    :param input_dir: str, 输入目录路径
    :param save_dir: str, 保存缩放后结果的目录
    :param average_abs_x_target: float, 目标 x 方向上的绝对值平均值
    :param average_abs_y_target: float, 目标 y 方向上的绝对值平均值
    :return: None
    """
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.npy'):
            file_path = os.path.join(input_dir, file_name)
            process_single_file(file_path, save_dir, average_abs_x_target, average_abs_y_target)

# 使用批量处理函数处理 ../npysave/ 目录下所有文件，并将结果保存到 ../npysave/scaled/ 目录
process_all_files('../npysave/', '../npysave/scaled/')

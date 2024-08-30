import numpy as np

# 加载数据
file_path = '../npysave/capital_j.npy'
tangent_vectors = np.load(file_path, allow_pickle=True)

# 初始化new_tangent_vectors
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

average_abs_x_current = np.mean(np.abs(new_tangent_vectors[:, 0]))
average_abs_y_current = np.mean(np.abs(new_tangent_vectors[:, 1]))

average_abs_x_target = 0.006000193767249584
average_abs_y_target = 0.01485129352658987

scale_x = average_abs_x_target / average_abs_x_current
scale_y = average_abs_y_target / average_abs_y_current

new_tangent_vectors[:, 0] *= scale_x
new_tangent_vectors[:, 1] *= scale_y

print("缩放后的new_tangent_vectors:")
print(new_tangent_vectors)

average_abs_x_final = np.mean(np.abs(new_tangent_vectors[:, 0]))
average_abs_y_final = np.mean(np.abs(new_tangent_vectors[:, 1]))
print(f"Final average_abs_x: {average_abs_x_final}, Final average_abs_y: {average_abs_y_final}")

# 保存缩放后的new_tangent_vectors
save_path = '../npysave/scaled/capital_j_scaled.npy'
np.save(save_path, new_tangent_vectors)
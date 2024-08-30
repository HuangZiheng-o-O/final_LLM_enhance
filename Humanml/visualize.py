import numpy as np
import matplotlib.pyplot as plt

# Load the numpy array from the uploaded file
file_path = './new_joint_vecs/012314.npy'
data = np.load(file_path)

# Extract root_linear_velocity from the data
# According to the updated knowledge, root_linear_velocity is located at indices 1 and 2
root_linear_velocity = data[:, 1:3]  # Extracting the root linear velocity (B, seq_len, 2)

# Calculate the cumulative sum to reconstruct the original trajectory in the XZ plane
trajectory_xz = np.cumsum(root_linear_velocity, axis=0)

# Plot the reconstructed trajectory
plt.figure(figsize=(8, 6))
plt.plot(trajectory_xz[:, 0], trajectory_xz[:, 1], label='Reconstructed Trajectory', marker='o')
plt.title('Reconstructed Root Joint Trajectory in XZ Plane')
plt.xlabel('X Position')
plt.ylabel('Z Position')
plt.grid(True)
plt.legend()
plt.show()

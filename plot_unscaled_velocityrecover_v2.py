import numpy as np
import matplotlib.pyplot as plt
import os
import glob
# Load the velocity data from the uploaded .npy file
npy_filename = '/Users/huangziheng/PycharmProjects/final_LLM_enhance/npysave/U_turn.npy'

try:
    # Load the velocity data from the .npy file
    root_linear_velocity = np.load(npy_filename)

    # Extract the velocity vectors from the loaded data
    velocity_vectors = root_linear_velocity.reshape(-1, 2)

    # Initialize the reconstructed points starting from the origin (0, 0)
    reconstructed_points = [(0, 0)]

    # Reconstruct the points using the velocity vectors
    for vx, vy in velocity_vectors:
        last_point = reconstructed_points[-1]
        new_point = (last_point[0] + vx, last_point[1] + vy)
        reconstructed_points.append(new_point)

    # Visualization
    plt.figure(figsize=(8, 6))
    plt.plot(*zip(*reconstructed_points), 'bx-', label='Reconstructed Points from Velocities')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Reconstructed Points from Velocity Vectors')
    plt.legend()
    plt.grid(True)
    plt.show()

except FileNotFoundError:
    print(f"Error: The file {npy_filename} does not exist. Please ensure the correct filename and path.")
except Exception as e:
    print(f"An error occurred while reading or processing the npy file: {e}")

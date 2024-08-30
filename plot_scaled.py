# Load the scaled velocity data from the uploaded .npy file
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

npy_filename_scaled = '/mnt/data/U_turn_scaled.npy'

try:
    # Load the velocity data from the .npy file
    root_linear_velocity_scaled = np.load(npy_filename_scaled)

    # Extract the velocity vectors from the loaded data
    velocity_vectors_scaled = root_linear_velocity_scaled.reshape(-1, 2)

    # Initialize the reconstructed points starting from the origin (0, 0)
    reconstructed_points_scaled = [(0, 0)]

    # Reconstruct the points using the velocity vectors
    for vx, vy in velocity_vectors_scaled:
        last_point = reconstructed_points_scaled[-1]
        new_point = (last_point[0] + vx, last_point[1] + vy)
        reconstructed_points_scaled.append(new_point)

    # Visualization
    plt.figure(figsize=(8, 6))
    plt.plot(*zip(*reconstructed_points_scaled), 'bx-', label='Reconstructed Points from Scaled Velocities')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Reconstructed Points from Scaled Velocity Vectors')
    plt.legend()
    plt.grid(True)
    plt.show()

except FileNotFoundError:
    print(f"Error: The file {npy_filename_scaled} does not exist. Please ensure the correct filename and path.")
except Exception as e:
    print(f"An error occurred while reading or processing the npy file: {e}")

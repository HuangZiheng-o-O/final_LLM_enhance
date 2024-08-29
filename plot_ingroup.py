import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Directory containing the .npy files
directory = 'npysave'

# Get a list of all .npy files in the directory
npy_files = glob.glob(os.path.join(directory, '*.npy'))

# Process each .npy file in the directory
for file_path in npy_files:
    # Load the tangent vectors from the .npy file
    tangent_vectors = np.load(file_path, allow_pickle=True)

    # Get the name from the file (without extension)
    type_name = os.path.splitext(os.path.basename(file_path))[0]

    # Extract the 200 tangent vectors (ignoring the batch dimension)
    tangent_vectors_extracted = tangent_vectors[0]

    # Initialize the starting point of the curve (assuming starting at origin)
    start_point = np.array([0, 0])
    points = [start_point]

    # Integrate the tangent vectors to get the points on the curve
    for tangent in tangent_vectors_extracted:
        # Compute the next point by adding the tangent vector to the current point
        next_point = points[-1] + tangent
        points.append(next_point)

    # Convert the list of points to a numpy array for easy plotting
    points = np.array(points)

    # Plot the reconstructed curve
    plt.figure(figsize=(8, 6))
    plt.plot(points[:, 0], points[:, 1], marker='o', linestyle='-', color='b', label='Reconstructed Curve')
    plt.title(f'Reconstructed Curve from Tangent Vectors - {type_name}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.axis('equal')

    # Save the plot as a PNG image
    plt.savefig(f'image/{type_name}.png')
    print(f"Saved plot for {type_name}.png")
    plt.close()

print("Processing complete for all .npy files in the '' directory.")

import numpy as np
import matplotlib.pyplot as plt

# Load the tangent vectors from the provided 'capital_W.npy' file
file_path = 'U_turn.npy'
tangent_vectors = np.load(file_path, allow_pickle=True)
# get name from file
type_name = file_path.split('.')[0]

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
plt.title('Reconstructed Curve from Tangent Vectors')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')
plt.show()
plt.savefig(f'image/{type_name}.png')


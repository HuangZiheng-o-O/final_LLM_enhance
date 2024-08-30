import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy.optimize import fsolve
from scipy.integrate import simps

# Generate approximately 30 input points for testing
original_points = [(i, np.sin(i / 2.0)) for i in np.linspace(0, 10, 30)]

def interpolate_and_resample_velocity2(original_points, num_output_points=200):
    x = np.array([p[0] for p in original_points], dtype=float)
    y = np.array([p[1] for p in original_points], dtype=float)

    # Apply a small perturbation to avoid duplicates
    x += np.random.normal(0, 1e-10, size=x.shape)
    y += np.random.normal(0, 1e-10, size=y.shape)

    # B-spline with small smoothing
    tck, u = splprep([x, y], s=1e-5)

    num_points = 2000  # Increase the number of points used for interpolation
    u_fine = np.linspace(0, 1, num_points)
    x_fine, y_fine = splev(u_fine, tck)

    # Using Simpson's rule for curve length calculation
    def curve_length(u1, u2):
        u1 = np.atleast_1d(u1)[0]  # Ensure u1 is scalar
        u2 = np.atleast_1d(u2)[0]  # Ensure u2 is scalar
        u_values = np.linspace(u1, u2, 100)
        derivatives = np.array(
            [np.sqrt((splev(u, tck, der=1)[0]) ** 2 + (splev(u, tck, der=1)[1]) ** 2) for u in u_values])
        length = simps(derivatives, u_values)
        return length

    total_length = curve_length(0, 1)
    segment_length = total_length / (num_output_points - 1)

    uniform_u = [0]
    for i in range(1, num_output_points):
        target_length = i * segment_length
        func = lambda u: curve_length(0, np.atleast_1d(u)[0]) - target_length  # Ensure u is scalar
        ui = fsolve(func, uniform_u[-1])[0]
        uniform_u.append(ui)

    uniform_points = [(splev(ui, tck)[0], splev(ui, tck)[1]) for ui in uniform_u]

    # Calculate velocity vectors between resampled points
    velocity_vectors = [(uniform_points[i][0] - uniform_points[i - 1][0],
                         uniform_points[i][1] - uniform_points[i - 1][1]) for i in range(1, len(uniform_points))]

    # Reconstruct points using velocity vectors starting from the first point
    reconstructed_points = [uniform_points[0]]
    for vx, vy in velocity_vectors:
        last_point = reconstructed_points[-1]
        new_point = (last_point[0] + vx, last_point[1] + vy)
        reconstructed_points.append(new_point)

    return reconstructed_points, velocity_vectors

# Resample and calculate velocities
reconstructed_points, velocity_vectors = interpolate_and_resample_velocity2(original_points, num_output_points=200)

# Visualization
plt.figure(figsize=(8, 6))
plt.plot(*zip(*original_points), 'ro-', label='Original Points')
plt.plot(*zip(*reconstructed_points), 'bx-', label='Reconstructed Points from Velocities')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Reconstructed Points Visualization')
plt.legend()
plt.grid(True)
plt.show()

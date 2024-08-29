import numpy as np
from scipy.interpolate import splprep, splev
from scipy.integrate import simps
from scipy.optimize import fsolve
# Function to parse keyframes from the text file
def parse_keyframes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    keyframes = []
    for line in lines:
        line = line.strip()
        if line.startswith("(") and line.endswith("),"):
            frame_data = eval(line.replace(';', ''))
            # Flattening the nested tuples
            if isinstance(frame_data[0], tuple):
                frame_data = frame_data[0]
            keyframes.append(frame_data)

    return keyframes



# Function to interpolate and resample velocities
def interpolate_and_resample_velocity(original_points):
    x = np.array([p[0] for p in original_points])
    y = np.array([p[1] for p in original_points])

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
        derivatives = np.array([np.sqrt((splev(u, tck, der=1)[0]) ** 2 + (splev(u, tck, der=1)[1]) ** 2) for u in u_values])
        length = simps(derivatives, u_values)
        return length

    total_length = curve_length(0, 1)
    segment_length = total_length / 199  # Divide total length into 200 segments for 200 points

    uniform_u = [0]
    for i in range(1, 200):
        target_length = i * segment_length
        func = lambda u: curve_length(0, np.atleast_1d(u)[0]) - target_length  # Ensure u is scalar
        ui = fsolve(func, uniform_u[-1])[0]
        uniform_u.append(ui)

    # Compute 2D velocities (tangent vectors) at the sampled points
    root_linear_velocity = []
    for ui in uniform_u:
        dx, dy = splev(ui, tck, der=1)  # First derivative gives the tangent vector
        root_linear_velocity.append((dx, dy))

    root_linear_velocity = np.array(root_linear_velocity)  # Convert to numpy array

    return root_linear_velocity

# Test the function with keyframes from the file
if __name__ == "__main__":
    # Read the keyframes from the text file
    keyframes_file = 'keyframes.txt'
    keyframes = parse_keyframes(keyframes_file)

    # Call the interpolate_and_resample_velocity function
    velocities = interpolate_and_resample_velocity(keyframes)

    # Save the velocities to a text file
    with open("velocities.txt", "w") as f:
        f.write("velocities = [\n")
        for i, (dx, dy) in enumerate(velocities):
            f.write(f"    ({i}, ({dx:.6f}, {dy:.6f})),\n")
        f.write("]\n")

    print("Velocities have been computed and saved to 'velocities.txt'.")

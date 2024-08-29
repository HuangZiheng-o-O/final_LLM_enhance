from scipy.interpolate import splprep, splev
from scipy.integrate import simps
from scipy.optimize import fsolve
import numpy as np

def interpolate_and_resample_velocity(original_points):
    x = np.array([p[0] for p in original_points])
    y = np.array([p[1] for p in original_points])

    # Apply a small perturbation to avoid duplicates
    x += np.random.normal(0, 1e-10, size=x.shape)
    y += np.random.normal(0, 1e-10, size=y.shape)

    # B-spline with no smoothing for better control around sharp turns
    tck, u = splprep([x, y], s=0)

    num_points = 2000
    u_fine = np.linspace(0, 1, num_points)
    x_fine, y_fine = splev(u_fine, tck)

    # Curve length calculation using Simpson's rule
    def curve_length(u1, u2):
        u_values = np.linspace(u1, u2, 100)
        derivatives = np.sqrt((splev(u_values, tck, der=1)[0]) ** 2 + (splev(u_values, tck, der=1)[1]) ** 2)
        length = simps(derivatives, u_values)
        return length

    total_length = curve_length(0, 1)
    segment_length = total_length / 199

    uniform_u = [0]

    # Ensure function passed to fsolve returns scalar and is vectorized
    def find_next_u(target_length, u_prev):
        func = lambda u: curve_length(0, u) - target_length
        return fsolve(func, u_prev)[0]

    for i in range(1, 200):
        target_length = i * segment_length
        next_u = find_next_u(target_length, uniform_u[-1])
        uniform_u.append(next_u)

    # Compute 2D velocities (tangent vectors) at the sampled points
    root_linear_velocity = []
    for ui in uniform_u:
        dx, dy = splev(ui, tck, der=1)
        root_linear_velocity.append((dx, dy))

    root_linear_velocity = np.array(root_linear_velocity)

    return root_linear_velocity

# Example usage
original_points =[
    (0, (0.0, 0.0)),
    (1, (0.7750302333648995, 1.5227473244609682)),
    (2, (1.5138209144018933, 2.76401608410098)),
    (3, (2.181827011972558, 3.4943587905494757)),
    (4, (2.747813303389942, 3.578772207526697)),
    (5, (3.1853148987159483, 3.0016525857561236)),
    (6, (3.4738747096012355, 1.8696800029213572)),
    (7, (3.6, 0.39209864084737145)),
    (8, (3.557793291511389, -1.157961825882429)),
    (9, (3.3492281229149428, -2.493974021023757)),
    (10, (2.9840567696906946, -3.3689772116757717)),
    (11, (2.4793542384566023, -3.621227792473302)),
    (12, (1.858719858636595, -3.2040974552804085)),
    (13, (1.1511738040454893, -2.194692392812222)),
    (14, (0.38980014181500655, -0.7796002836300135)),
    (15, (-0.3898001418150061, -0.7796002836300127)),
    (16, (-1.1511738040454906, -2.194692392812224)),
    (17, (-1.8587198586365967, -3.20409745528041)),
    (18, (-2.4793542384566027, -3.6212277924733023)),
    (19, (-2.984056769690694, -3.368977211675772)),
    (20, (-3.3492281229149428, -2.493974021023757)),
    (21, (-3.5577932915113895, -1.157961825882428)),
    (22, (-3.6, 0.39209864084737234)),
    (23, (-3.473874709601235, 1.869680002921359)),
    (24, (-3.1853148987159474, 3.0016525857561254)),
    (25, (-2.7478133033899397, 3.578772207526698)),
    (26, (-2.181827011972556, 3.494358790549475)),
    (27, (-1.5138209144018946, 2.764016084100981)),
    (28, (-0.7750302333649008, 1.522747324460969)),
    (29, (-4.440892098500626e-16, 8.881784197001252e-16)),
]
  # Define your original keyframe points here
velocities = interpolate_and_resample_velocity(original_points)

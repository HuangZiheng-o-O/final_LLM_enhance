import numpy as np
import math
from typing import List, Tuple
from scipy.interpolate import splprep, splev
from scipy.integrate import simps
from scipy.optimize import fsolve


def execute_code_and_compute_keyframes(extracted_code: str, log_file: str = "./log/model_interaction_log.txt") -> List[
    Tuple[int, Tuple[float, float]]]:

    # Prepare the namespace for executing the extracted code
    local_vars = {}

    # Debugging: Print extracted code
    print("Extracted code:\n", extracted_code)

    # Execute the extracted code in the provided local_vars namespace
    exec(extracted_code, {"np": np, "math": math}, local_vars)  # Pass np and math into the exec context

    # Extract the shape_curve function and t_range from local_vars
    shape_curve = local_vars.get('shape_curve')
    t_range = local_vars.get('t_range')


    if not shape_curve or not t_range:
        raise ValueError("shape_curve function or t_range was not found in the extracted code.")

    # Step 2: Sample Points from the Curve
    numberOfPoints = 30
    t_values = np.linspace(t_range[0], t_range[1], numberOfPoints)  # Use custom t_range
    sampled_points = [shape_curve(ti) for ti in t_values]

    # Step 3: Normalize and scale the sampled points to fit within the specified range [-3.6, 3.6]
    x_values = np.array([point[0] for point in sampled_points])
    y_values = np.array([point[1] for point in sampled_points])

    x_min, x_max = np.min(x_values), np.max(x_values)
    y_min, y_max = np.min(y_values), np.max(y_values)

    if x_min == x_max:
        x_scaled = np.zeros_like(x_values)  # All x-values are the same, no need to scale
    else:
        x_scaled = 7.2 * (x_values - x_min) / (x_max - x_min) - 3.6

    if y_min == y_max:
        y_scaled = np.zeros_like(y_values)  # All y-values are the same, no need to scale
    else:
        y_scaled = 7.2 * (y_values - y_min) / (y_max - y_min) - 3.6

    x0, y0 = x_scaled[0], y_scaled[0]
    x_scaled = x_scaled - x0
    y_scaled = y_scaled - y0

    keyframes = list(zip(range(len(x_scaled)), zip(x_scaled, y_scaled)))

    # Save keyframes in the desired format
    with open("keyframes.txt", "w") as f:
        f.write("kframes = [\n")
        for frame in keyframes:
            f.write(f"    {frame},\n")
        f.write("]\n")

    return keyframes


# Testing the function
if __name__ == "__main__":
    # Read the shape_curve function and t_range from the text file
    with open("shape_curve.txt", "r", encoding="utf-8") as file:
        extracted_code = file.read()

    # Call the function with the extracted code
    execute_code_and_compute_keyframes(extracted_code)

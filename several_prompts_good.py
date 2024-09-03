import os
import math
import yaml
import re
import numpy as np
import matplotlib.pyplot as plt

from typing import List, Tuple
from scipy.integrate import simps, quad
from scipy.interpolate import splprep, splev
from scipy.optimize import fsolve
import numpy as np
from scipy.interpolate import splprep, splev
from scipy.integrate import simps
from scipy.optimize import fsolve
from openai import OpenAI
# Load API key from a YAML configuration file
with open("config.yaml") as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)

# Set the API key and model name
MODEL = "gpt-4o-mini"
# MODEL = "gpt-4o"

client = OpenAI(api_key=config_yaml['token'])


def replace_placeholders(instruct_content: str, descriptions: List[str]) -> str:
    for i, description in enumerate(descriptions):
        instruct_content = instruct_content.replace(f"placeholder{i + 1}", description.strip())
    return instruct_content
def format_keyframes(keyframes: list, pattern_name="origin_30points",keyframes_str = "keyframes_str") -> str:
    pattern_name = pattern_name+"_"+keyframes_str
    # Initialize the formatted string with the pattern name
    formatted_string = f'elif pattern == "{pattern_name}":\n    kframes = [\n'

    # Iterate over the list of keyframes and format each one
    for frame in keyframes:
        # Each frame should be a tuple like (frame_number, (x_coordinate, y_coordinate))
        frame_num, coordinates = frame
        x_coord, y_coord = coordinates
        x_coord = round(float(x_coord), 2)
        y_coord = round(float(y_coord), 2)

        # Append the formatted frame to the string
        formatted_string += f'        ({frame_num}, ({x_coord:.2f}, {y_coord:.2f})),\n'

    # Close the list
    formatted_string += '    ]'

    return formatted_string

# def replace_placeholders_one(follow_up_question: str, keyframes: list) -> str:
#     # Round the coordinates to two decimal places
#     keyframes_rounded = [(frame, (round(x, 2), round(y, 2))) for frame, (x, y) in keyframes]
#
#     # Convert the list of keyframes to a string representation
#     keyframes_str = ', '.join([f"Frame {frame}: ({x}, {y})" for frame, (x, y) in keyframes_rounded])
#
#     # Replace the placeholder with the keyframes string
#     follow_up_question = follow_up_question.replace("PALCEHOLDER1", keyframes_str)
#     return follow_up_question
#


# pattern_name is "PALCEHOLDER2"
def replace_pattern_name(follow_up_question: str, pattern_name: str) -> str:
    # Replace the placeholder with the keyframes string
    follow_up_question = follow_up_question.replace("PALCEHOLDER2", pattern_name)
    return follow_up_question


def extract_code_block(text: str) -> str:
    # 尝试提取带语言说明的代码块
    code_block_match = re.search(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1).strip()
    # 备用: 提取不带语言说明的代码块
    code_block_match = re.search(r'```\n(.*?)\n```', text, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1).strip()
    return text

def interpolate_and_resample(original_points):
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
    segment_length = total_length / 29

    uniform_u = [0]
    for i in range(1, 30):
        target_length = i * segment_length
        func = lambda u: curve_length(0, np.atleast_1d(u)[0]) - target_length  # Ensure u is scalar
        ui = fsolve(func, uniform_u[-1])[0]
        uniform_u.append(ui)

    uniform_points = [(splev(ui, tck)[0], splev(ui, tck)[1]) for ui in uniform_u]
    return uniform_points

def execute_code_and_compute_keyframes(extracted_code: str, log_file: str = "./log/model_interaction_log.txt") -> List[Tuple[int, Tuple[float, float]]]:
    def log_to_file(message: str):
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(message + "\n")
    # Prepare the namespace for executing the extracted code
    local_vars = {}
    # Debugging: Print extracted code
    print("Extracted code:\n", extracted_code)

    # Execute the extracted code in the provided local_vars namespace
    exec(extracted_code, {"np": np, "math": math}, local_vars)  # Pass np and math into the exec context

    # Extract the shape_curve function and t_range from local_vars
    shape_curve = local_vars.get('shape_curve')
    t_range = local_vars.get('t_range')
    log_to_file(f"shape_curve_I_got: {shape_curve}")
    log_to_file(f"t_range_I_got: {t_range}")

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

    return list(zip(x_scaled, y_scaled))


    # # Step 4: Assign Frame Numbers
    # frames = np.linspace(0, 115, len(sampled_points), dtype=int)
    # keyframes = list(zip(frames, zip(x_scaled, y_scaled)))
    #
    # # Write keyframes to Result.txt
    # with open('Result.txt', 'w', encoding='utf-8') as file:
    #     for frame, (x, y) in keyframes:
    #         file.write(f"Frame {frame}: ({x:.2f}, {y:.2f})\n")
    #
    # return keyframes
    #


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

def inside(
        instruct_content: str,
        descriptions: List[str],
        follow_up_question_file: str = "./prompt/follow_up_question.txt",  # Path to the file with the follow-up question
        log_file: str = "./log/model_interaction_log.txt"  # Path to the log file
) -> str:
    # Function to log messages to the log file
    def log_to_file(message: str):
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(message + "\n")

    print(descriptions)

    # Read the follow-up question from the file
    with open(follow_up_question_file, 'r', encoding='utf-8') as file:
        follow_up_question = file.read().strip()

    # Initial dialog with the first question
    dialogs = [
        {"role": "user", "content": instruct_content},
    ]

    # Log the initial user instruction
    log_to_file(f"User: {instruct_content}")

    # Generate the response for the first question
    completion = client.chat.completions.create(
        model=MODEL,
        messages=dialogs
    )
    first_response = completion.choices[0].message.content
    print(first_response)

    # Log the model's first response
    log_to_file(f"Model: {first_response}")

    # Extract the Python code block from the first response
    extracted_code = extract_code_block(first_response)
    log_to_file(f"extracted_code: {extracted_code}")
    # Execute the extracted code and compute keyframes
    # Define a list of functions to check for
    import numpy as np

    # Define a list of functions to check for
    math_functions = ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'exp', 'log']

    # Function to replace math functions with numpy versions
    def replace_math_functions(code):
        for func in math_functions:
            if func in code and f'np.{func}' not in code:
                code = code.replace(func, f'np.{func}')
        return code

    try:
        original_points = execute_code_and_compute_keyframes(extracted_code)

    except Exception as e:
        log_to_file(f"Error executing code: {e}")
        # Attempt to replace math functions only if there was an error
        extracted_code = replace_math_functions(extracted_code)
        try:
            original_points = execute_code_and_compute_keyframes(extracted_code)
        except Exception as e:
            log_to_file(f"Error executing code after replacement: {e}")
            return "\nI encountered an error while executing the code. Please try again with a different input."


    except Exception as e:
        log_to_file(f"Error executing code: {e}")
        return f"\nI encountered an error while executing the code.Please try again with a different input."


    # Extract the pattern name from the descriptions
    my_pattern_name = descriptions[0].split(":")[0]
    # my_pattern_name如果有\n 去掉
    my_pattern_name = my_pattern_name.replace("\n"," ")

    # Modify the follow-up question
    follow_up_question = replace_pattern_name(follow_up_question, my_pattern_name)

    dialogs.append({"role": "user", "content": follow_up_question})

    # Generate the response to the second question
    completion = client.chat.completions.create(
        model=MODEL,
        messages=dialogs
    )

    new_pattern_name = completion.choices[0].message.content

    #这里原来是saple了30个点，现在改成200个点而且是速度
    # interpolate_and_resample_velocity(original_points)
    try:
        _, tangent_vectors = interpolate_and_resample_velocity2(original_points)
        tangent_vectors_array = np.array(tangent_vectors)
        root_linear_velocity = tangent_vectors_array.reshape(1, len(tangent_vectors), 2)
        print(root_linear_velocity.shape)  # Should print: (1, seq_len, 2)
        # np.save(f"{new_pattern_name}.npy", root_linear_velocity) save to the directory "/npysave"
        np.save(f"./npysave/{new_pattern_name}.npy", root_linear_velocity)
        print("#######################\n")
        print("root_linear_velocity: ", str(root_linear_velocity))
        print("#######################\n")
    except Exception as e:
        log_to_file(f"Error interpolating velocity: {e}")
         #{new_pattern_name}
        log_to_file(f"Error interpolating velocity: {new_pattern_name}")
        return f"\nI encountered an error while interpolating velocity. Please try again with a different input."


    return root_linear_velocity





def log_results(result_file_path: str, descriptions: List[str], result: str):
    with open(result_file_path, 'a', encoding='utf-8') as file:
        file.write("\n")
        file.write(result)
        file.write("\n")


def main():

    instruct_file_path = './prompt/ChainPrompt.txt'
    trajectories_file_path = './prompt/trajectories.txt'
    result_file_path = './result/newResult.txt'


    with open(instruct_file_path, 'r', encoding='utf-8') as file:
        original_instruct_content = file.read()

    # Read the content of trajectories.txt
    with open(trajectories_file_path, 'r', encoding='utf-8') as file:
        trajectories = file.readlines()

    total_lines = len(trajectories)
    index = 0

    while index < total_lines:
        descriptions = trajectories[index:index + 1]
        if len(descriptions) < 1 or not any(descriptions):
            break
        instruct_content = replace_placeholders(original_instruct_content, descriptions)
        result = inside(instruct_content=instruct_content,descriptions=descriptions)

        log_results(result_file_path, descriptions, str(result))
        index += 1


if __name__ == "__main__":
    os.environ['WORLD_SIZE'] = '1'
    main()

import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# Define a function to parse the keyframes.txt file
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

# Define the function to save the image
def save_image(keyframes, pattern_name, save_dir='.'):
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = os.path.join(save_dir, f"{current_time}_{pattern_name}.png")

    fig, ax = plt.subplots(figsize=(10, 6))

    if keyframes:
        # Debugging: Print keyframes
        print(f"Keyframes for pattern '{pattern_name}': {keyframes}")

        try:
            # Unpack the tuples correctly
            x_vals = [coord[0] for frame, coord in keyframes]
            y_vals = [coord[1] for frame, coord in keyframes]
        except ValueError as e:
            print(f"Error unpacking keyframes for pattern '{pattern_name}': {e}")
            return

        norm = Normalize(vmin=0, vmax=len(x_vals) - 1)
        cmap = plt.get_cmap('viridis')
        sm = ScalarMappable(cmap=cmap, norm=norm)
        colors = sm.to_rgba(range(len(x_vals) - 1))

        for i in range(len(x_vals) - 1):
            ax.plot(x_vals[i:i + 2], y_vals[i:i + 2], color=colors[i], marker='o')
            ax.quiver(x_vals[i], y_vals[i], x_vals[i + 1] - x_vals[i], y_vals[i + 1] - y_vals[i],
                      angles='xy', scale_units='xy', scale=1, color=colors[i])

    ax.set_xlim(min(x_vals) - 1, max(x_vals) + 1)
    ax.set_ylim(min(y_vals) - 1, max(y_vals) + 1)
    ax.set_aspect('auto')
    ax.grid(True)

    # Set the title of the plot to the pattern name
    ax.set_title(f'Pattern: {pattern_name}')

    plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.02, pad=0.04)

    plt.savefig(image_filename)
    print(f"Image saved to: {image_filename}")
    # plt.show()

# Option 1: Generate image for the keyframes in keyframes.txt
def generate_image_for_keyframes(file_path, save_dir='.'):
    keyframes = parse_keyframes(file_path)
    if keyframes:
        save_image(keyframes, 'keyframes', save_dir)
    else:
        print("No keyframes found.")

# Example usage
pattern_file = './keyframes.txt'  # Update this path if needed
save_dir = './imagesGPT'  # Directory where images will be saved

# Generate image for the keyframes in keyframes.txt
generate_image_for_keyframes(pattern_file, save_dir)

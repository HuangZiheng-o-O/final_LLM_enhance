
import os
import openai
import yaml

import re


import json
import re

# Load API key from a YAML configuration file
with open("config.yaml") as f:
 config_yaml = yaml.load(f, Loader=yaml.FullLoader)

# Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=config_yaml['token'])

# Set the model name
MODEL = "gpt-4o-mini"

def llm(prompt, stop=["\n"]):
    # Prepare the dialog for the API request
    dialogs = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model=MODEL,
        messages=dialogs
    )
    return completion.choices[0].message.content

def generate_fine_motion_think_prompt(original_action):
    prompt = f"""
    The action '{original_action}' may require detailed control over specific body parts. 
    Please evaluate the action and think carefully about how the movement breaks down into smaller steps. 
    You should independently decide the steps involved in completing this action.

    After thinking, provide a structured list of the steps involved in performing this action.
    When your thinking is done, say '<DONE>'.

    Now think:
    """
    return prompt

def generate_sequence_explanation_prompt(original_action):
    prompt = f"""
    Based on your breakdown of the action '{original_action}', provide a concise explanation for each of the steps you identified.
    For each step, analyze:
    - The dynamic movement
    - The necessary coordination between body parts

    Do not include the Expression.Focus on the action and movement itself.
    When your explanation is finished, say '<SEQUENCEEND>'.
    """
    return prompt

def generate_sequence_explanation_prompt_json(sequence_explanation_prompt):
    prompt = f"""
    Based on your breakdown of the action '{sequence_explanation_prompt}', evaluate fine motion control for the following body parts:

    For each step, analyze:
    - The dynamic movement of whole body.
    - spine: [Action description]
    - Left Arm: [Action description]
    - Right Arm: [Action description]
    - Left Leg: [Action description]
    - Right Leg: [Action description]

    Ensure the explanation is in the following JSON-like format for each body part:
    {{
        "body part": "spine",
        "description": "Description of the movement of the spine."
    }},
    {{
        "body part": "Left Arm",
        "description": "Description of the movement of the left arm."
    }},
    {{
        "body part": "Right Arm",
        "description": "Description of the movement of the right arm."
    }},
    {{
        "body part": "Left Leg",
        "description": "Description of the movement of the left leg."
    }},
    {{
        "body part": "Right Leg",
        "description": "Description of the movement of the right leg."
    }}

    Focus only on these body parts. DO NOT include any details about facial expressions, eyes, or emotions. 
    Be concise and AVOID providing any reasoning or explanation—focus only on the action of each body part.

    When you finish the explanation for all steps, say '<SEQUENCEEND>'.
    """
    return prompt

def sequence_analyze(action):
    sequence_explanation_prompt = generate_sequence_explanation_prompt(action)
    sequence_explanation = llm(sequence_explanation_prompt, stop=["<SEQUENCEEND>"]).split("<SEQUENCEEND>")[0].strip()
    print(sequence_explanation)

    # Use the updated format to generate JSON-like output for each body part
    sequence_explanation_prompt2 = generate_sequence_explanation_prompt_json(sequence_explanation)
    print(sequence_explanation_prompt2)

    sequence_explanation2 = llm(sequence_explanation_prompt2, stop=["<SEQUENCEEND>"]).split("<SEQUENCEEND>")[0].strip()

    # Formatting the output into the desired JSON-like format for each body part
    output = (
            "Action: " + action + "\n" +
            sequence_explanation2 + "\n" +
            "\n"
    )

    # Write to file
    with open("sequence_explanation.txt", "a") as file:
        file.write(output)

    # Print to console
    print(output)

    # Return results as well
    return sequence_explanation2

txt = sequence_analyze("Perform a signature James Bond pose with a dramatic turn and gunpoint.")
print("done")

########################


########################

print("11")
def generate_fine_motion_control_prompt(original_action, sequence_explanation):
    prompt = f"""
Now, based on the action '{original_action}' and the {sequence_explanation}, evaluate fine motion control for the following body parts:

- spine
- left arm
- right arm
- left leg
- right leg

For each body part, provide a short, concise action description in the following JSON format:

{{
  "body part": "<body part>",
  "description": "<action description>"
}}

Focus only on what needs to be done, avoiding explanations or reasoning. Do not include any details about facial expressions, eyes, or emotions. Keep it concise and avoid phrases like "to ensure" or "providing support and balance."
I do not like vague terms, such as "at an appropriate angle" (because I cannot tell what angle is appropriate), or "Adjust the right arm for balance" (because I do not know how to adjust for balance). I prefer specific action descriptions, such as "Raise the right arm to shoulder height" (because I know exactly what shoulder height is). Please ensure the descriptions are clear and specific.
Output one JSON object per body part as shown above.

When you finish, say '<CONTROLEND>'.
"""
    return prompt

def analyze_fine_moton_control_txt(action):
    # Step 1: Get sequence explanation
    sequence_explanation_prompt = generate_sequence_explanation_prompt(action)
    sequence_explanation = llm(sequence_explanation_prompt, stop=["<SEQUENCEEND>"]).split("<SEQUENCEEND>")[0].strip()

    # Step 2: Evaluate fine motion control
    fine_moton_control_prompt = generate_fine_motion_control_prompt(action, sequence_explanation)
    control_evaluation = llm(fine_moton_control_prompt, stop=["<CONTROLEND>"]).split("<CONTROLEND>")[0].strip()

    # Parse the JSON objects from the control evaluation
    json_objects = re.findall(r'\{[^}]+\}', control_evaluation)
    control_results = [json.loads(obj) for obj in json_objects]

    # Output to file as well as print
    # output = {
    #     "Action": action,
    #     "Sequence Explanation": sequence_explanation,
    #     "Fine Motion Control Evaluation": control_results
    # }
    output = control_results

    # Write to file
    with open("analyze_fine_moton_control.json", "a") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)
        file.write("\n")

    # Print to console
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # Return results as well
    return sequence_explanation, control_results

actions_to_test = [
    "Perform a signature James Bond pose with a dramatic turn and gunpoint.",
    # "Fight with the fluid precision and power of Bruce Lee.",
]

# Test each action and save the results in the JSON file
for action in actions_to_test:
    sequence_explanation, control_results = analyze_fine_moton_control_txt(action)
print("22")
########################


def check_trajectory_control_with_llm(action):
    # First call: Let the LLM think using chain of thought reasoning
    first_prompt = f"""
    Examine the action: "{action}".

    Trajectory control is only necessary if the action includes explicit instructions for movement along a specific two-dimensional path. This typically includes instructions like "turn", "move in a circle", "zigzag", or "change direction", which clearly involve a shift in direction or orientation.

    If an action involves simple movement in a straight line (such as "run forward" or "jump in place") or basic rotations (like "spin in place"), trajectory control is not required because there is no complex or changing path to follow.

    Consider whether the action explicitly requires a change in direction or follows a curved or angular path, then conclude if trajectory control is necessary. If the path is simple or linear, trajectory control is not needed.

    Explain your reasoning step by step and conclude with whether trajectory control is required.
    """

    first_response = llm(first_prompt)

    # Second call: Ask LLM to give a simple boolean response based on its reasoning
    second_prompt = f"""
Based on your previous analysis: "{first_response}", answer with only 'True' if trajectory control is required, and 'False' if it is not.
"""
    second_response = llm(second_prompt).strip()

    return second_response


# Convert the second response to a boolean value
def response_to_bool(response):
    if response.lower() == "true":
        return True
    elif response.lower() == "false":
        return False
    else:
        raise ValueError("Unexpected response from LLM: " + response)

#
# # List of action cases to test
# actions = [
#     "Run forward, then jump in place",                       # Example 1
#     "Walk forward and make a left turn",                     # Example 2
#     "Stand still and wave your hand",                        # Example 3
#     "Run up, then kneel and slide backward",                 # Example 4
#     "Walk around in a circle",                               # Example 5
#     "Spin in place on one foot",                             # Example 6
#     "Crawl under the table",                                 # Example 7
#     "Run forward and stop at the door",                      # Example 8
#     "Jump forward and then turn around",                     # Example 9
#     "Dance freely with no set path",                         # Example 10
#     "Climb up the ladder",                                   # Example 11
#     "Roll on the ground twice",                              # Example 12
#     "Run forward, kneel, and slide in a straight line",      # Example 13
#     "Hop in a zigzag pattern",                               # Example 14
#     "Jump sideways then spin 180 degrees",                   # Example 15
#     "Walk straight then stop and jump on one leg",           # Example 16
#     "Swim forward in a straight line",                       # Example 17
#     "Skate in a figure-eight pattern",                       # Example 18
#     "Step backward three times then kneel",                  # Example 19
#     "Jump forward and spin in a circle mid-air"              # Example 20
# ]
#
# # Test trajectory control for each action using LLM
# for action in actions:
#     print(f"Action: {action}")
#     reasoning = check_trajectory_control_with_llm(action)
#     result_bool = response_to_bool(reasoning)
#     print(f"Needs Trajectory Control: {result_bool}")
#     print("=======================================")

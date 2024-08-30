import numpy as np

# Load the numpy file to read its contents
file_path = './new_joint_vecs/012314.npy'
data = np.load(file_path, allow_pickle=True)

# Display the type and shape of the data to understand its structure
data_type = type(data)
data_shape = data.shape if hasattr(data, 'shape') else None

print(data_type, data_shape)


import pandas as pd

# Convert the numpy array to a pandas DataFrame for better visualization if it's a 2D array
if len(data.shape) == 2:
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(data)

#save the dataframe to a csv file
df.to_csv('data.csv', index=False)
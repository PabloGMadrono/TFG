import numpy as np
import matplotlib.pyplot as plt

# Load CSV file with encoding fix
file_path = "data/mapaTFG.csv"  # Replace with your actual file path
data = np.loadtxt(file_path, delimiter=";", dtype=int, encoding="utf-8-sig")

# Define colors: 0 -> Light Blue, 1 -> Dark Blue, 2 -> Yellow
colors = {
    0: [0.4, 0.8, 0.9],  # Light Blue
    1: [0.1, 0.1, 0.3],  # Dark Blue
    2: [1.0, 1.0, 0.2]   # Yellow
}

# Convert data values to color map
colored_map = np.array([[colors[val] for val in row] for row in data])

# Display the image
plt.imshow(colored_map, interpolation="nearest")
plt.axis("off")  # Hide axes
plt.show()

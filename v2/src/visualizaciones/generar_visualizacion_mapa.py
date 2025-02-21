import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from v2.src.files_management.file_names import map_file
# Load CSV file with encoding fix

def generar_visualizacion_mapa(map_file=map_file):
    data = pd.read_csv(map_file, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()

    # Define colors: 0 -> Light Blue, 1 -> Dark Blue, 2 -> Yellow
    colors = {
        0: [0.4, 0.8, 0.9],  # Light Blue
        1: [0.1, 0.1, 0.3],  # Dark Blue
        2: [1.0, 1.0, 0.2],  # Yellow
        99: [0.3, 0.3, 0.3]
    }

    # Convert data values to color map
    colored_map = np.array([[colors[val] for val in row] for row in data])

    # Display the image
    plt.imshow(colored_map, interpolation="nearest")
    plt.axis("off")  # Hide axes
    plt.show()


def main():
    generar_visualizacion_mapa()




if __name__ == '__main__':
    main()

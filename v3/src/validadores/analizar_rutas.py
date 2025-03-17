from v3.src.files_management.json_management import load_file, save_file
from v3.src.files_management.file_names import optimized_route_file, visualization_dir, statistics_dir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



def generate_statistics(products_file, route_file, name):
    data = load_file(route_file)

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Convert "Number of products" to integer (it comes as a string)
    df["Number of products"] = df["Number of products"].astype(int)

    # Compute basic statistics
    summary_stats = df[["Number of products", "total_distance", "execution_time"]].describe().to_dict()
    algorithm_counts = df["algorithm"].value_counts().to_dict()

    avg_distance = df["total_distance"].mean()
    avg_time = df["execution_time"].mean()

    corr_distance = df["Number of products"].corr(df["total_distance"])
    corr_time = df["Number of products"].corr(df["execution_time"])

    follows_percentage = df["Follows regla de oro"].mean() * 100

    # Print statistics to console
    print("===== Summary Statistics =====")
    print(summary_stats)
    print("\n===== Algorithm Counts =====")
    print(algorithm_counts)
    print(f"\nAverage Total Distance: {avg_distance:.2f}")
    print(f"Average Execution Time: {avg_time:.2f} seconds")
    print(f"\nCorrelation between Number of Products and Total Distance: {corr_distance:.2f}")
    print(f"Correlation between Number of Products and Execution Time: {corr_time:.2f}")
    print(f"\nPercentage of orders following 'regla de oro': {follows_percentage:.2f}%")

    # Calculate average execution time per algorithm
    avg_exec_time = df.groupby("algorithm")["execution_time"].mean().to_dict()
    print("Average execution time per algorithn:", avg_exec_time)

    # Load the products file data which contains gondolas and products info
    products_data = load_file(products_file)
    # Number of gondolas is the number of nodes in the file
    number_of_gondolas = len(products_data)
    # Total number of products is the sum of the products in each gondola
    total_number_of_products = sum(len(gondola["list_of_products"]) for gondola in products_data)

    print(f"\nTotal number of gondolas (nodes): {number_of_gondolas}")
    print(f"Total number of products (from products file): {total_number_of_products}")

    # Prepare a dictionary with statistics to save as JSON
    stats = {
        "summary_statistics": summary_stats,
        "algorithm_counts": algorithm_counts,
        "average_total_distance": avg_distance,
        "average_execution_time": avg_time,
        "correlation_num_products_total_distance": corr_distance,
        "correlation_num_products_execution_time": corr_time,
        "percentage_following_regla_de_oro": follows_percentage,
        "average_execution_time_per_algorithm": avg_exec_time,
        "number_of_gondolas (nodes)": number_of_gondolas,
        "total_number_of_products": total_number_of_products
    }


    stats_file = os.path.join(statistics_dir, "execution_statistics"+str(name)+".json")
    save_file(stats_file, stats)



    # -------------------- Visualizations --------------------
    # First figure: multiple subplots
    plt.figure(figsize=(12, 8))

    # Distribution of total distance
    plt.subplot(2, 2, 1)
    plt.hist(df["total_distance"], bins=10, color='skyblue', edgecolor='black')
    plt.xlabel("Total Distance")
    plt.ylabel("Frequency")
    plt.title("Distribution of Total Distance")

    # Distribution of execution time
    plt.subplot(2, 2, 2)
    plt.hist(df["execution_time"], bins=10, color='lightgreen', edgecolor='black')
    plt.xlabel("Execution Time (s)")
    plt.ylabel("Frequency")
    plt.title("Distribution of Execution Time")

    # Scatter plot: Number of products vs Total Distance
    plt.subplot(2, 2, 3)
    plt.scatter(df["Number of products"], df["total_distance"], color='red')
    plt.xlabel("Number of Products")
    plt.ylabel("Total Distance")
    plt.title("Products vs Total Distance")

    # Scatter plot: Number of products vs Execution Time
    plt.subplot(2, 2, 4)
    plt.scatter(df["Number of products"], df["execution_time"], color='purple')
    plt.xlabel("Number of Products")
    plt.ylabel("Execution Time (s)")
    plt.title("Products vs Execution Time")

    plt.tight_layout()
    vis_file1 = os.path.join(visualization_dir, "route_statistics"+str(name)+".png")
    plt.savefig(vis_file1)
    plt.close()
    print(f"Visualization saved to {vis_file1}")

    # Create a single figure with two subplots side by side
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

    # First Plot: Algorithm Usage Distribution
    pd.Series(algorithm_counts).plot(kind="bar", color="orange", edgecolor='black', ax=axes[0])
    axes[0].set_xlabel("Algorithm")
    axes[0].set_ylabel("Count of Orders")
    axes[0].set_title("Algorithm Usage Distribution")

    # Second Plot: Average Execution Time per Algorithm
    pd.Series(avg_exec_time).plot(kind="bar", color="blue", edgecolor='black', ax=axes[1])
    axes[1].set_xlabel("Algorithm")
    axes[1].set_ylabel("Average Execution Time (s)")
    axes[1].set_title("Average Execution Time per Algorithm")

    plt.tight_layout()
    vis_file = os.path.join(visualization_dir, "algorithm_comparison"+str(name)+".png")
    plt.savefig(vis_file)
    plt.close()
    print(f"Visualization saved to {vis_file}")


def main():
    generate_statistics()



if __name__ == '__main__':
    main()
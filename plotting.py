import numpy as np
import matplotlib.pyplot as plt

def plot_points_with_distances_and_path(distances, shortest_path):
    num_points = len(distances)

    # Generate random coordinates for points
    points = np.random.rand(num_points, 2)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot points
    for i, point in enumerate(points):
        ax.scatter(*point, label=f'Point {i + 1}')

    # Plot connections based on distances
    for i in range(num_points):
        for j in range(i + 1, num_points):
            distance = distances[i, j]
            point_i, point_j = points[i], points[j]
            ax.plot([point_i[0], point_j[0]], [point_i[1], point_j[1]], linestyle='-', linewidth=1, color='gray')
            ax.text((point_i[0] + point_j[0]) / 2, (point_i[1] + point_j[1]) / 2, f'{distance:.2f}', color='red')

    # Plot the shortest path
    for edge in shortest_path:
        i, j = edge
        point_i, point_j = points[i], points[j]
        ax.plot([point_i[0], point_j[0]], [point_i[1], point_j[1]], linestyle='-', linewidth=2, color='green')

    # Set labels and legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Points with Connections, Distances, and Shortest Path')
    ax.legend()

    # Show the plot
    plt.show()

# Example usage
distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

shortest_path = [(4, 2), (2, 1), (1, 0), (0, 3), (3, 4)]

plot_points_with_distances_and_path(distances, shortest_path)

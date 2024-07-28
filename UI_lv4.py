import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Define the map
city_map = [
    [0, 0, 0, -1, -1, 0, 0, 0, 0, 0],
    [0, 'S1', 0, 0, 0, 0, 0, -1, 0, -1],
    [0, 0, -1, -1, -1, 'S2', 0, -1, 0, -1],
    [0, 0, 0, 0, -1, 0, 0, -1, 0, 0],
    [0, 0, -1, -1, -1, 0, 'G3', -1, -1, 0],
    [1, 0, -1, 0, 0, 0, 0, 0, -1, 0],
    [0, 0, 'F1', 0, 1, 4, -1, 8, -1, 0],
    [0, 0, 0, 0, -1, 0, 0, 0, 'G1', 0],
    [0, -1, -1, -1, 'S3', 0, 0, 0, 0, 0],
    ['G2', 0, 5, 0, 0, 0, -1, -1, -1, 0]
]

# Define the colors for each type of cell
colors = {
    0: 'white',
    -1: 'gray',
    'S1': 'lightgreen',
    'S2': 'lightgreen',
    'S3': 'lightgreen',
    'G1': 'lightcoral',
    'G2': 'lightcoral',
    'G3': 'lightcoral',
    'F1': 'lightblue',
    1: 'lightblue',
    4: 'yellow',
    5: 'lightblue',
    8: 'orange'
}

# Define the paths
paths = [
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (7, 5), (7, 6), (7, 7), (7, 8)],
    [(2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (9, 0)],
    [(8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (4, 6)]
]

# Define colors for each path
path_colors = ['green', 'red', 'blue']

# Variables to manage path steps and current path index
current_step = 0
current_path_index = 0

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)

# Plot the grid and fill the cells
def draw_map():
    ax.clear()
    for i in range(len(city_map)):
        for j in range(len(city_map[0])):
            cell_value = city_map[len(city_map) - 1 - i][j]
            color = colors.get(cell_value, 'white')
            ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=color, edgecolor='black'))
            if cell_value not in [0, -1]:
                ax.text(j + 0.5, i + 0.5, str(cell_value), ha='center', va='center', fontsize=12, 
                        bbox=dict(facecolor='white', edgecolor='none', pad=0.5))

# Plot the paths up to the current step
def draw_paths(step):
    for path_index in range(len(paths)):
        path = paths[path_index][:step + 1]
        if len(path) < 2:
            continue
        
        y, x = zip(*path)
        x = [xi + 0.5 for xi in x]
        y = [len(city_map) - yi - 0.5 for yi in y]
        ax.plot(x, y, color=path_colors[path_index], linewidth=2)
        ax.scatter(x[-1], y[-1], color=path_colors[path_index], s=100)  # Mark the current position

    ax.set_aspect('equal')
    ax.set_xlim(0, len(city_map[0]))
    ax.set_ylim(0, len(city_map))
    ax.set_xticks(np.arange(0, len(city_map[0]) + 1, 1))
    ax.set_yticks(np.arange(0, len(city_map) + 1, 1))
    ax.grid(which='both', color='black', linestyle='-', linewidth=2)
    ax.axis('off')

draw_map()
draw_paths(current_step)

# Button to go to the next step
axnext = plt.axes([0.8, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')

# Button to go to the previous step
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
bprev = Button(axprev, 'Previous')

# Functions to handle button clicks
def next(event):
    global current_step
    if current_step < len(paths[current_path_index]) - 1:
        current_step += 1
        draw_map()
        draw_paths(current_step)
        plt.draw()

def prev(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        draw_map()
        draw_paths(current_step)
        plt.draw()

bnext.on_clicked(next)
bprev.on_clicked(prev)

plt.show()

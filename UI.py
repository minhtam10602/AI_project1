import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Define the map
city_map = [
    [0, 0, -1, -1, 0, 0, 0, 0, 0, 0],
    ['S', 0, 0, 0, 0, 0, 0, 0, -1, 0],
    [0, -1, -1, -1, -1, 0, -1, 0, -1, 0],
    [0, 0, -1, 0, 0, 0, 'G', -1, -1, 0],
    [1, 0, -1, 0, 0, 0, -1, 0, -1, 0],
    [0, 0, 0, 1, 4, -1, 8, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -1, -1, -1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['G', 0, 5, 0, 0, -1, -1, -1, -1, 0]
]

# Define the colors for each type of cell
colors = {
    0: 'white',
    -1: 'gray',
    'S': 'lightgreen',
    'G': 'lightcoral',
    1: 'lightblue',
    4: 'yellow',
    5: 'lightblue',
    8: 'orange'
}

# Define the paths
paths = [
    [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (5, 2), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (9, 0) ]
]

# Variables to manage path steps
current_step = 0

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

# Plot the path up to the current step
def draw_path(step):
    path = paths[0][:step + 1]
    y, x = zip(*path)  # Swap x and y
    x = [xi + 0.5 for xi in x]
    y = [len(city_map) - yi - 0.5 for yi in y]  # Correct coordinate transformation
    ax.plot(x, y, color='green', linewidth=2)
    ax.scatter(x[-1], y[-1], color='green', s=100)  # Mark the current position
    ax.set_aspect('equal')
    ax.set_xlim(0, len(city_map[0]))
    ax.set_ylim(0, len(city_map))
    ax.set_xticks(np.arange(0, len(city_map[0]) + 1, 1))
    ax.set_yticks(np.arange(0, len(city_map) + 1, 1))
    ax.grid(which='both', color='black', linestyle='-', linewidth=2)
    ax.axis('off')

draw_map()
draw_path(current_step)

# Button to go to the next step
axnext = plt.axes([0.8, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')

# Button to go to the previous step
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
bprev = Button(axprev, 'Previous')

# Functions to handle button clicks
def next(event):
    global current_step
    if current_step < len(paths[0]) - 1:
        current_step += 1
        draw_map()
        draw_path(current_step)
        plt.draw()

def prev(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        draw_map()
        draw_path(current_step)
        plt.draw()

bnext.on_clicked(next)
bprev.on_clicked(prev)

plt.show()

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.colors import TABLEAU_COLORS

def parse_city_map(file_path_level1):
    with open(file_path_level1, 'r') as file:
        lines = file.readlines()
    
    # Read the first line to get the dimensions of the map
    dimensions = lines[0].strip().split()
    width, height = int(dimensions[0]), int(dimensions[1])
    
    city_map = []
    for line in lines[1:]:
        city_map.append([int(x) if x.isdigit() or x == '-1' else x for x in line.strip().split()])
        
    return city_map, width, height

# Define the map
file_path = 'input_level1.txt'
city_map, width, height = parse_city_map(file_path)

# Define specific colors for 'S' and 'G' cells
special_colors = {
    'S': 'firebrick', 'G': 'firebrick',
    'S1': 'firebrick', 'G1': 'firebrick',
    'S2': 'sienna', 'G2': 'sienna',
    'S3': 'darkorange', 'G3': 'darkorange',
    'S4': 'yellow', 'G4': 'yellow',
    'S5': 'palegreen', 'G5': 'palegreen',
    'S6': 'lime', 'G6': 'lime',
    'S7': 'steelblue', 'G7': 'steelblue',
    'S8': 'blueviolet', 'G8': 'blueviolet',
    'S9': 'orchid', 'G9': 'orchid'
}

# Automatically generate colors for each unique cell type except 0 and -1
unique_cells = set(cell for row in city_map for cell in row if cell not in [0, -1])
colors = {cell: color for cell, color in zip(unique_cells, TABLEAU_COLORS)}

# Manually set colors for 0 and -1 cells
colors[0] = 'white'
colors[-1] = 'gray'

# Add special colors to the colors dictionary
colors.update(special_colors)

# Define the paths
paths = [
    [(1, 0) ,(2, 0) ,(3, 0) ,(4, 0) ,(5, 0), (6, 0), (7, 0), (8, 0), (9, 0)]
]

# Define colors for each path
path_colors = ['firebrick', 'sienna', 'darkorange', 'yellow', 'palegreen', 'lime', 'steelblue', 'blueviolet', 'orchid']

# Variables to manage path steps and current path index
current_step = 0
current_path_index = 0

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)

# Plot the grid and fill the cells
def draw_map():
    ax.clear()
    for i in range(height):
        for j in range(width):
            try:
                cell_value = city_map[height - 1 - i][j]
                color = colors.get(cell_value, 'white')
                ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=color, edgecolor='black'))
                if cell_value not in [0, -1, '0', '-1']:
                    ax.text(j + 0.5, i + 0.5, str(cell_value), ha='center', va='center', fontsize=12, 
                            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
            except IndexError as e:
                continue

def draw_paths(step):
    for path_index in range(len(paths)):
        path = paths[path_index][:step + 1]
        if len(path) < 2:
            continue
        
        y, x = zip(*path)
        x = [xi + 0.5 for xi in x]
        y = [len(city_map) - yi - 0.5 for yi in y]
        ax.plot(x, y, color=path_colors[path_index], linewidth=2)
        ax.scatter(x[-1], y[-1], color=path_colors[path_index], s=100)

    ax.set_aspect('equal')
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks(np.arange(0, width + 1, 1))
    ax.set_yticks(np.arange(0, height + 1, 1))
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

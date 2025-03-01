import matlab.engine
import time
import os
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from models.py import best_fit_plane
# Start MATLAB Engine
eng = matlab.engine.start_matlab()

# Define image path
image_path = "static/images/graph.png"

# Initialize x, y, z values
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
z = [2, 4, 6, 8, 10]

# Convert to MATLAB format
x_mat = matlab.double(x)
y_mat = matlab.double(y)
z_mat = matlab.double(z)

# Create figure and plot **(only once)**
eng.figure('Visible', 'off', nargout=0)  # Hide the figure
graph_handle = eng.plot3(x_mat, y_mat, z_mat, 'o-', 'LineWidth', 2, nargout=1)

eng.xlabel('X Values', nargout=0)
eng.ylabel('Y Values', nargout=0)
eng.zlabel('Z Values', nargout=0)
eng.title('3D Live Graph', nargout=0)
eng.grid('on', nargout=0)

# Loop to update data **without displaying a graph**
while True:
    # Add new random points
    x.append(randint(1, 50))
    y.append(randint(1, 50))
    z.append(randint(1, 50))

    # Convert updated lists to MATLAB arrays
    x_mat = matlab.double(x)
    y_mat = matlab.double(y)
    z_mat = matlab.double(z)

    # Update the existing plot (do not create a new figure)
    eng.set(graph_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

    # Save the updated graph **without opening MATLAB**
    eng.saveas(eng.gcf(), image_path, 'png', nargout=0)

    print("Graph updated and saved.")

    # Wait 1 second before updating
    time.sleep(1)

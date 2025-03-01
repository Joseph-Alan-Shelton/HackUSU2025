import matlab.engine
import time
import os
from random import randint
# Start MATLAB Engine
eng = matlab.engine.start_matlab()

# Define image path
image_path = "static/images/graph.png"

# Initialize x-values

x = [1, 2, 3, 4, 5]  # Replace with your x values
y = [2, 4, 6, 8, 10]  # Replace with your y values
z = [2, 4, 6, 8, 10]
while True:
    x.append(randint(1,50))
    y.append(randint(1,50))
    z.append(randint(1,50))
    x_mat = matlab.double(x)
    y_mat = matlab.double(y)
    z_mat = matlab.double(z)

    # Plot in MATLAB
    eng.figure(nargout=0)
    eng.plot3(x_mat, y_mat,z_mat, 'o-', 'LineWidth', 2, nargout=0)
    eng.xlabel('X Values', nargout=0)
    eng.ylabel('Y Values', nargout=0)
    eng.zlabel('Z Values', nargout=0)
    eng.title('X vs Y Plot', nargout=0)
    eng.grid('on', nargout=0)

    eng.saveas(eng.gcf(), 'static/images/graph.png', 'png', nargout=0)
    print(f"Updated Graph:points")

    # Wait 1 second before updating
    time.sleep(1)

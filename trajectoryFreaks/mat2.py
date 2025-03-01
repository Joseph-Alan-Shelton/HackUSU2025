import matlab.engine
import time
import os
from random import randint
import numpy as np
from models import best_fit_plane  # Import the best-fit plane function
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import SQL from basicServer
from basicServer import SQL

# Start MATLAB Engine
eng = matlab.engine.start_matlab()

# Define image path
image_path = "static/images/graph.png"

# Initialize x, y, z values
print(1)
s=SQL()
print(2)
q= f"""
        SELECT * FROM RpoPlan ORDER BY (select Null) OFFSET ? ROWS FETCH NEXT ? ROWS ONLY;
        """
x = s.query(q,(1000,5000))
xposTotal=[row[14] for row in x]
yposTotal=[row[15] for row in x]
zposTotal=[row[16] for row in x]
xpos=[xposTotal[0]]
ypos=[yposTotal[0]]
zpos=[zposTotal[0]]
# Convert to MATLAB format
x_mat = matlab.double(xpos)
y_mat = matlab.double(ypos)
z_mat = matlab.double(zpos)

# Create MATLAB figure **(only once)**
eng.figure('Visible', 'off', nargout=0)  # Hide the figure
scatter_handle = eng.scatter3(x_mat, y_mat, z_mat, 50, 'b', 'filled', nargout=1)  # Scatter plot
eng.xlabel('X Values', nargout=0)
eng.ylabel('Y Values', nargout=0)
eng.zlabel('Z Values', nargout=0)
eng.title('3D Live Graph with Best-Fit Plane', nargout=0)
eng.grid('on', nargout=0)
eng.hold('on', nargout=0)  # Keep scatter points when adding the plane

# Variable to store plane handle
plane_handle = None  # Initially no plane

# Loop to update data **without deleting the scatter plot**
for i in range(1,len(xposTotal)):
    # Add new random points
    xpos.append(xposTotal[i])
    ypos.append(yposTotal[i])
    zpos.append(zposTotal[i])

    # Convert updated lists to MATLAB arrays
    x_mat = matlab.double(xpos)
    y_mat = matlab.double(ypos)
    z_mat = matlab.double(zpos)

    # Update scatter plot data without deleting it
    eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

    # Compute best-fit plane
    _, equation = best_fit_plane(xpos, ypos, zpos)
    

    # Extract coefficients (z = Ax + By + C)
    A, B, C = equation[0], equation[1], equation[2]

    # Generate a mesh grid for the plane
    x_fit = np.linspace(min(xpos), max(xpos), 10)
    y_fit = np.linspace(min(ypos), max(ypos), 10)
    X_fit, Y_fit = np.meshgrid(x_fit, y_fit)
    Z_fit = A * X_fit + B * Y_fit + C  # Compute Z from the plane equation

    # Convert plane data to MATLAB format
    X_mat = matlab.double(X_fit.tolist())
    Y_mat = matlab.double(Y_fit.tolist())
    Z_mat = matlab.double(Z_fit.tolist())

    # **Delete the old plane before adding the new one** (prevents overlapping planes)
    if plane_handle:
        eng.delete(plane_handle, nargout=0)  # Delete old plane

    # Add the new best-fit plane
    plane_handle = eng.surf(X_mat, Y_mat, Z_mat, 'FaceAlpha', 0.5, 'EdgeColor', 'none', nargout=1)  # 50% transparency

    # Save the updated graph **without opening MATLAB**


    

    # Wait 1 second before updating
    time.sleep(.001)
    eng.saveas(eng.gcf(), image_path, 'png', nargout=0)
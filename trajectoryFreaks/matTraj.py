import matlab.engine
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from basicServer import SQL
def best_fit_plane(x, y, z):
    """Fits a best-fit plane to given 3D points and returns the plot and equation."""

    # Convert input to numpy arrays
    x, y, z = np.array(x), np.array(y), np.array(z)

    # Create the design matrix for linear regression (Ax + By + C = Z)
    A = np.column_stack((x, y, np.ones_like(x)))
    
    # Solve for coefficients [A, B, C] in the equation z = Ax + By + C
    C, _, _, _ = np.linalg.lstsq(A, z, rcond=None)

    # Generate surface for visualization
    x_fit = np.linspace(min(x), max(x), 10)
    y_fit = np.linspace(min(y), max(y), 10)
    X_fit, Y_fit = np.meshgrid(x_fit, y_fit)
    Z_fit = C[0] * X_fit + C[1] * Y_fit + C[2]  # Compute best-fit plane

    # Plot data points and best-fit plane
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, color='blue', label='Original Data')
    ax.plot_surface(X_fit, Y_fit, Z_fit, alpha=0.5, color='r')

    # Labels and title
    ax.set_xlabel('X Values')
    ax.set_ylabel('Y Values')
    ax.set_zlabel('Z Values')
    ax.set_title('Best-Fit Plane in 3D')
    ax.legend()

    # Generate the best-fit plane equation as a string
    equation = f"z = {C[0]:.4f}x + {C[1]:.4f}y + {C[2]:.4f}"
    plt.close(fig)
    return fig, C # Returns the figure and equation string


def main(lower, upper):
    eng = matlab.engine.start_matlab()

    # Define a point and direction for the line
    point = matlab.double([1, 2, 3])  # Starting point (x0, y0, z0)
    direction = matlab.double([2, -1, 1])  # Direction vector (a, b, c)
    t_range = matlab.double([-5, 5])  # Range for parameter t
    eng.addpath(r'C:\path\to\your\matlab\functions', nargout=0)  

    # Call MATLAB function
    eng.draw3DLine(point, direction, t_range, nargout=0)

    # Save figure
    IMAGE_PATH = "static/images/3Dline.png"
    eng.saveas(eng.gcf(), IMAGE_PATH, 'png', nargout=0)

    eng.close()



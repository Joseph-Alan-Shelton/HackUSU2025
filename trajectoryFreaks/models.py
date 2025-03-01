from django.db import models
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def best_fit_plane(x, y, z):
    """
    Fits a best-fit plane (linear polynomial) to given 3D points (x, y, z) using least squares regression.

    Args:
        x (list or np.array): X coordinates
        y (list or np.array): Y coordinates
        z (list or np.array): Z coordinates

    Returns:
        tuple: (coefficients, best-fit plane equation as string)
    """

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

    plt.show()

    # Return coefficients and equation as a string
    equation = f"z = {C[0]:.4f}x + {C[1]:.4f}y + {C[2]:.4f}"
    return C, equation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main(lower, upper):
    # Define the semi-major and semi-minor axes
    r1 = 50  # Stretch along X
    r2 = 10  # Stretch along Y

    t = np.linspace(lower, upper, 500)  # More points for smoothness

    # Define elliptical parametric equations
    x = r1 * np.cos(t) 
    y = 0 # Instead of fixed y=0
    z = r2 * np.sin(t)   # Optional height variation

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D elliptical curve
    ax.plot(x, y, z, '.', linewidth=.1, label="3D Elliptical Polynomial Curve")

    # Labels and title
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title("3D Elliptical Polynomial Curve")
    ax.legend()
    ax.grid(True)

    # Fix aspect ratio (prevents stretching)
    max_range = max(r1, r2, abs(upper))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    # Save figure
    IMAGE_PATH = "static/images/ellipse_fixed.png"
    plt.savefig(IMAGE_PATH)

    plt.show()

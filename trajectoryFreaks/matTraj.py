import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basicServer import SQL

def best_fit_plane(x, y, z):
    """Fits a best-fit plane to given 3D points and returns the plane equation coefficients."""
    
    # Convert to numpy arrays
    x, y, z = np.array(x), np.array(y), np.array(z)

    # Design matrix for Ax + By + C = Z
    A = np.column_stack((x, y, np.ones_like(x)))
    
    # Solve for coefficients A, B, C
    C, _, _, _ = np.linalg.lstsq(A, z, rcond=None)

    return tuple(C)  # Returns (A, B, C)

def main(lower, upper):
    print(f"Running main() with bounds: {lower}s - {upper}s")

    # Define image path
    IMAGE_PATH = "static/images/graph.png"

    # Initialize SQL connection and query data
    s = SQL()
    q = """
    SELECT positionChiefEciX, positionChiefEciY, positionChiefEciZ, positionDeputyEciX, positionDeputyEciY, positionDeputyEciZ FROM RpoPlan 
    WHERE ? <= secondsSinceStart AND secondsSinceStart <= ? ;
    """
    x = s.query(q, (lower, upper))
    s.close()
    print("Finished query")
    curr = time.time()

    # Extract Deputy positions
    deputyXpos = [row[3] for row in x]
    deputyYpos = [row[4] for row in x]
    deputyZpos = [row[5] for row in x]

    # Extract Chief positions
    chiefXpos = [row[0] for row in x]
    chiefYpos = [row[1] for row in x]
    chiefZpos = [row[2] for row in x]

    # Define the semi-major and semi-minor axes for the elliptical dots
    r1 = 45000000  # Stretch along X
    r2 = 42000000  # Stretch along Z
    t = np.linspace(lower, upper, 500)  # More points for smoothness

    # Define elliptical parametric equations
    x_ellipse = r1 * np.cos(t)
    y_ellipse = r2 * np.sin(t)
    
    z_ellipse =  (r2/113 * np.sin(t))  # Lifts the ellipse up


    # Compute min/max for Deputy and Ellipse Z-values
    deputy_z_min = min(deputyZpos) if deputyZpos else None
    deputy_z_max = max(deputyZpos) if deputyZpos else None
    ellipse_z_min = min(z_ellipse)
    ellipse_z_max = max(z_ellipse)

    # Compute best-fit plane coefficients
    A, B, C = best_fit_plane(deputyXpos, deputyYpos, deputyZpos)

    # Generate a mesh grid for the best-fit plane
    x_min, x_max = min(deputyXpos), max(deputyXpos)
    y_min, y_max = min(deputyYpos), max(deputyYpos)

    X_fit, Y_fit = np.meshgrid(
        np.linspace(x_min, x_max, 10),
        np.linspace(y_min, y_max, 10)
    )
    Z_fit = A * X_fit + B * Y_fit + C  # Compute Z values for the plane

    # Create 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot Deputy scatter plot (Blue)
    ax.scatter(deputyXpos, deputyYpos, deputyZpos, color='blue', marker='.', s=10, label="Deputy Positions")

    # Plot Chief scatter plot (Red)
    ax.scatter(chiefXpos, chiefYpos, chiefZpos, color='red', marker='.', s=10, label="Chief Positions")

    # Plot the 3D elliptical curve using dots (Green)
    ax.scatter(x_ellipse, y_ellipse, z_ellipse, color='green', marker='.', s=5, label="3D Elliptical Dots")

    # Plot the best-fit plane
    ax.plot_surface(X_fit, Y_fit, Z_fit, alpha=0.5, cmap='Reds', edgecolor='none', label="Best-Fit Plane")

    # Labels and title
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")
    ax.set_title("Combined 3D Graph: Positions, Elliptical Dots, and Best-Fit Plane")
    ax.legend()
    ax.grid(True)

    max_range = max(r1, r2, abs(upper), max(deputyXpos, default=0), max(chiefXpos, default=0))
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
   

    # Save figure
    plt.savefig(IMAGE_PATH)



    elapsed = time.time() - curr
    print(f"Total elapsed time: {elapsed:.2f} seconds")

    # Return min and max values
    result = {
        "deputy_z_min": deputy_z_min,
        "deputy_z_max": deputy_z_max,
        "ellipse_z_min": ellipse_z_min,
        "ellipse_z_max": ellipse_z_max
    }

    print("Computed Z-Value Ranges:")
    print(f"  Deputy Z Min: {result['deputy_z_min']}")
    print(f"  Deputy Z Max: {result['deputy_z_max']}")
    print(f"  Ellipse Z Min: {result['ellipse_z_min']}")
    print(f"  Ellipse Z Max: {result['ellipse_z_max']}")

    



    return result

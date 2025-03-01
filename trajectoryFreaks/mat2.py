import matlab.engine
import os
import numpy as np
import sys
import time
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

    x_range = np.linspace(np.min(x), np.max(x), 10)
    y_range = np.linspace(np.min(y), np.max(y), 10)
    X_fit, Y_fit = np.meshgrid(x_range, y_range)
    Z_fit = C[0] * X_fit + C[1] * Y_fit + C[2]  # Compute best-fit plane

    # Plot data points and best-fit plane
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, color='blue', label='Original Data')
    ax.plot_surface(X_fit, Y_fit, Z_fit, alpha=0.5, cmap='Reds')

    # Labels and title
    ax.set(xlabel='X Values', ylabel='Y Values', zlabel='Z Values', title='Best-Fit Plane in 3D')
    ax.legend()

    # Return figure and plane coefficients
    plt.close(fig)
    return fig, tuple(C)  # Returns figure and (A, B, C)


def main(lower, upper):
    print(f"Running main() with bounds: {lower}s - {upper}s")

    # Add parent directory to sys.path

    # Start MATLAB Engine
    eng = matlab.engine.start_matlab()

    # Define image path
    IMAGE_PATH = "static/images/graph.png"

    # Initialize SQL connection and query data
    s = SQL()
    q = """
    SELECT positionChiefEciX, positionChiefEciY, positionChiefEciZ, positionDeputyEciX, positionDeputyEciY, positionDeputyEciZ FROM RpoPlan 
    WHERE ? <= secondsSinceStart AND secondsSinceStart <= ? ;    """
    x = s.query(q, (lower, upper))
    s.close()
    print("finished query")
    curr = time.time()
    # Extract timestamps
    
    # --------------------------- Plot Deputy ---------------------------
    deputyXpos = [row[3] for row in x]
    deputyYpos = [row[4] for row in x]
    deputyZpos = [row[5] for row in x]

    # Create MATLAB figure (only once)
    eng.figure('Visible', 'off', nargout=0)  
    deputy_positions = matlab.double([deputyXpos, deputyYpos, deputyZpos])
    scatter_handle = eng.scatter3(*deputy_positions, 50, 'b', 'filled', nargout=1)

    # Set graph properties
    eng.eval("xlabel('X Values'); ylabel('Y Values'); zlabel('Z Values'); title('3D Live Graph with Best-Fit Plane'); grid on; hold on;", nargout=0)

    # Compute best-fit plane
    _, (A, B, C) = best_fit_plane(deputyXpos, deputyYpos, deputyZpos)  # Direct unpacking


    # Generate a mesh grid for the plane
    # Generate a mesh grid for the plane
    x_min, x_max = min(deputyXpos), max(deputyXpos)
    y_min, y_max = min(deputyYpos), max(deputyYpos)

    X_fit, Y_fit = np.meshgrid(
        np.linspace(x_min, x_max, 5), 
        np.linspace(y_min, y_max, 5)
    )

    Z_fit = A * X_fit + B * Y_fit + C  # Ensure Z_fit is a 2D matrix

    # Add best-fit plane
    eng.surf(
        matlab.double(X_fit.tolist()), 
        matlab.double(Y_fit.tolist()), 
        matlab.double(Z_fit.tolist()), 
        'FaceAlpha', 0.5, 'EdgeColor', 'none', nargout=1
    )

    # --------------------------- Plot Chief ---------------------------
    chiefXpos = [row[0] for row in x]
    chiefYpos = [row[1] for row in x]
    chiefZpos = [row[2] for row in x]

    # Create Chief's scatter plot (Red)
    deputy_positions = matlab.double([chiefXpos, chiefYpos, chiefZpos])
    scatter_handle = eng.scatter3(*deputy_positions, 50, 'r', 'o', nargout=1)

    # Save the updated graph
    eng.saveas(eng.gcf(), IMAGE_PATH, 'png', nargout=0)
    elapsed = time.time() - curr
    print(f"Total elapsed time: {elapsed:.2f} seconds")


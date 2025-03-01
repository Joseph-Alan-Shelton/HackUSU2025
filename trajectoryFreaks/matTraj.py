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
    print(f"RAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHH{lower}s - {upper}s")

    # Add parent directory to sys.path

    # Start MATLAB Engine
    eng = matlab.engine.start_matlab()

    # Define image path
    IMAGE_PATH = "static/images/graph.png"

    # Initialize SQL connection and query data
    s = SQL()
    q = """
    SELECT * FROM RpoPlan 
    WHERE ? <= secondsSinceStart AND secondsSinceStart <= ? 
    ORDER BY (SELECT NULL);
    """
    x = s.query(q, (lower, upper))
    s.close()
    # Extract timestamps
    times = [row[0] for row in x]


    deputyXpos = [row[14] for row in x]
    deputyYpos = [row[15] for row in x]
    deputyZpos = [row[16] for row in x]
    chiefXpos = [row[8] for row in x]
    chiefYpos = [row[9] for row in x]
    chiefZpos = [row[10] for row in x]

    deputyXposTemp = []
    deputyYposTemp = []
    deputyZposTemp = []
    chiefXposTemp = []
    chiefYposTemp = []
    chiefZposTemp = []
    # Create MATLAB figure (only once)
    eng.figure('Visible', 'off', nargout=0)  
    

    # Set graph properties
    eng.xlabel('X Values', nargout=0)
    eng.ylabel('Y Values', nargout=0)
    eng.zlabel('Z Values', nargout=0)
    eng.title('3D Live Graph with Best-Fit Plane', nargout=0)
    eng.grid('on', nargout=0)
    eng.hold('on', nargout=0)

    for i in range(len(times)):
        print(i)
        # --------------------------- Plot Deputy ---------------------------
        deputyXposTemp.append(deputyXpos[i])
        deputyYposTemp.append(deputyYpos[i])
        deputyZposTemp.append(deputyZpos[i])
        chiefXposTemp.append(chiefXpos[i])
        chiefYposTemp.append(chiefYpos[i])
        chiefZposTemp.append(chiefZpos[i])

        scatter_handle_2 = eng.scatter3(
        matlab.double(deputyXposTemp), 
        matlab.double(deputyYposTemp), 
        matlab.double(deputyZposTemp), 
        50, 'b', 'filled', nargout=1
        )
        # Compute best-fit plane
        _, equation = best_fit_plane(deputyXposTemp, deputyYposTemp, deputyZposTemp)
        A, B, C = equation[0], equation[1], equation[2]

        # Generate a mesh grid for the plane
        x_fit = np.linspace(min(deputyXposTemp), max(deputyXposTemp), 10)
        y_fit = np.linspace(min(deputyYposTemp), max(deputyYposTemp), 10)
        X_fit, Y_fit = np.meshgrid(x_fit, y_fit)
        Z_fit = A * X_fit + B * Y_fit + C

        # Add best-fit plane
        eng.surf(
        matlab.double(X_fit.tolist()), 
        matlab.double(Y_fit.tolist()), 
        matlab.double(Z_fit.tolist()), 
        'FaceAlpha', 0.5, 'EdgeColor', 'none', nargout=1
        )

        # --------------------------- Plot Chief ---------------------------


        # Create Chief's scatter plot (Red)
        scatter_handle = eng.scatter3(
        matlab.double(chiefXposTemp), 
        matlab.double(chiefYposTemp), 
        matlab.double(chiefZposTemp), 
        50, 'r', 'o', nargout=1
        )
        eng.view(3, nargout=0)

        # Save the updated graph
        eng.saveas(eng.gcf(), IMAGE_PATH, 'png', nargout=0)


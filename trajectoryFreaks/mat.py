import matlab.engine
import os
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

# Initialize sql connection
lowerbound = 662500
upperbound = 663000
s = SQL()

# Get the positions within our bounds
q = f"""
    SELECT * FROM RpoPlan 
    WHERE ? <= secondsSinceStart And secondsSinceStart <= ? 
    ORDER BY (select Null);
    """
rpoData = s.query(q,(lowerbound, upperbound))

# Get the times for each position
rpoTimes = [row[0] for row in rpoData]

# Plot Deputy-----------------------------------------------------------------------
# Get Deputy's positions from the sheet
deputyXpos = [row[14] for row in rpoData]
deputyYpos = [row[15] for row in rpoData]
deputyZpos = [row[16] for row in rpoData]

# Convert to MATLAB format
x_mat = matlab.double(deputyXpos[0])
y_mat = matlab.double(deputyYpos[0])
z_mat = matlab.double(deputyZpos[0])

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

# Convert updated lists to MATLAB arrays
x_mat = matlab.double(deputyXpos)
y_mat = matlab.double(deputyYpos)
z_mat = matlab.double(deputyZpos)

# Update scatter plot data without deleting it
eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

# Plot Chief--------------------------------------------------------------------------
# Get Deputy's positions from the sheet
chiefXpos=[row[8] for row in rpoData]
chiefYpos=[row[9] for row in rpoData]
chiefZpos=[row[10] for row in rpoData]

# Convert to MATLAB format
x_mat = matlab.double(chiefXpos[0])
y_mat = matlab.double(chiefYpos[0])
z_mat = matlab.double(chiefZpos[0])

# Create MATLAB figure **(only once)**
scatter_handle = eng.scatter3(x_mat, y_mat, z_mat, 50, 'r', 'o', nargout=1)  # Scatter plot

# Convert updated lists to MATLAB arrays
x_mat = matlab.double(chiefXpos)
y_mat = matlab.double(chiefYpos)
z_mat = matlab.double(chiefZpos)

# Update scatter plot data without deleting it
eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

# Compute best-fit plane for Deputy ----------------------------------------------------------
_, equation = best_fit_plane(deputyXpos, deputyYpos, deputyZpos)

# Extract coefficients (z = Ax + By + C)
A, B, C = equation[0], equation[1], equation[2]

# Generate a mesh grid for the plane
x_fit = np.linspace(min(deputyXpos), max(deputyXpos), 10)
y_fit = np.linspace(min(deputyYpos), max(deputyYpos), 10)
X_fit, Y_fit = np.meshgrid(x_fit, y_fit)
Z_fit = A * X_fit + B * Y_fit + C  # Compute Z from the plane equation

# Convert plane data to MATLAB format
X_mat = matlab.double(X_fit.tolist())
Y_mat = matlab.double(Y_fit.tolist())
Z_mat = matlab.double(Z_fit.tolist())

# Add the new best-fit plane
plane_handle = eng.surf(X_mat, Y_mat, Z_mat, 'FaceAlpha', 0.5, 'EdgeColor', 'none', nargout=1)  # 50% transparency

# Highlight points when maneuvers occur -------------------------------------------------------------
# Get the times of maneuvers that occur within our bounds
q = f"""
    SELECT positionDeputyEciX,positionDeputyEciY,positionDeputyEciZ FROM ManeuverPlan JOIN RpoPlan 
    on ManeuverPlan.secondsSinceStart = RpoPlan.secondsSinceStart 
    where ? <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= ? 
    ORDER BY (select RpoPlan.secondsSinceStart);
    """
maneuverPositions = s.query(q,(lowerbound, upperbound))

# Find the coordinates of every maneuver time
xManeuvers = [row[0] for row in maneuverPositions]
yManeuvers = [row[1] for row in maneuverPositions]
zManeuvers = [row[2] for row in maneuverPositions]

# If there are any manuevers in these bounds, plot them
if xManeuvers:
    # Convert to MATLAB format
    x_mat = matlab.double(xManeuvers[0])
    y_mat = matlab.double(yManeuvers[0])
    z_mat = matlab.double(zManeuvers[0])

    # Create MATLAB figure
    scatter_handle = eng.scatter3(x_mat, y_mat, z_mat, 50, 'm', 'filled', nargout=1)  # Scatter plot

    # Convert updated lists to MATLAB arrays
    x_mat = matlab.double(xManeuvers)
    y_mat = matlab.double(yManeuvers)
    z_mat = matlab.double(zManeuvers)

    # Update scatter plot data without deleting it
    eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

# Highlight points ground contact is available --------------------------------------------------------
# Get the times of maneuvers that occur within our bounds
q = f"""
    SELECT positionDeputyEciX,positionDeputyEciY,positionDeputyEciZ FROM GroundContacts JOIN RpoPlan 
    on GroundContacts.startSeconds <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= GroundContacts.stopSeconds
    where ? <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= ?
    ORDER BY (select RpoPlan.secondsSinceStart);
    """
groundContactPositions = s.query(q,(lowerbound, upperbound))

# Find the coordinates of every maneuver time
xGrountContacts = [row[0] for row in groundContactPositions]
yGrountContacts = [row[1] for row in groundContactPositions]
zGrountContacts = [row[2] for row in groundContactPositions]

# If there are any manuevers in these bounds, plot them
if xGrountContacts:
    # Convert to MATLAB format
    x_mat = matlab.double(xGrountContacts[0])
    y_mat = matlab.double(yGrountContacts[0])
    z_mat = matlab.double(zGrountContacts[0])

    # Create MATLAB figure
    scatter_handle = eng.scatter3(x_mat, y_mat, z_mat, 50, 'g', 'filled', nargout=1)  # Scatter plot

    # Convert updated lists to MATLAB arrays
    x_mat = matlab.double(xGrountContacts)
    y_mat = matlab.double(yGrountContacts)
    z_mat = matlab.double(zGrountContacts)

    # Update scatter plot data without deleting it
    eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)


# Highlight points payload is expected --------------------------------------------------------
# Get the times of maneuvers that occur within our bounds
q = f"""
    SELECT positionDeputyEciX,positionDeputyEciY,positionDeputyEciZ FROM PayloadEvents JOIN RpoPlan 
    on PayloadEvents.startSeconds <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= PayloadEvents.stopSeconds
    where ? <= RpoPlan.secondsSinceStart And RpoPlan.secondsSinceStart <= ?
    ORDER BY (select RpoPlan.secondsSinceStart);
    """
payloadPositions = s.query(q,(lowerbound, upperbound))

# Find the coordinates of every maneuver time
xPayloads = [row[0] for row in payloadPositions]
yPayloads = [row[1] for row in payloadPositions]
zPayloads = [row[2] for row in payloadPositions]

# If there are any manuevers in these bounds, plot them
if xPayloads:
    # Convert to MATLAB format
    x_mat = matlab.double(xPayloads[0])
    y_mat = matlab.double(yPayloads[0])
    z_mat = matlab.double(zPayloads[0])

    # Create MATLAB figure
    scatter_handle = eng.scatter3(x_mat, y_mat, z_mat, 50, 'c', 'filled', nargout=1)  # Scatter plot

    # Convert updated lists to MATLAB arrays
    x_mat = matlab.double(xPayloads)
    y_mat = matlab.double(yPayloads)
    z_mat = matlab.double(zPayloads)

    # Update scatter plot data without deleting it
    eng.set(scatter_handle, 'XData', x_mat, 'YData', y_mat, 'ZData', z_mat, nargout=0)

# Save the updated graph **without opening MATLAB**
eng.saveas(eng.gcf(), image_path, 'png', nargout=0)
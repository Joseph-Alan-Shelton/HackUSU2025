import matlab.engine
import os
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basicServer import SQL

def main(lower, upper):
    print(f"Running main() with bounds: {lower}s - {upper}s")

    # Start MATLAB Engine
    eng = matlab.engine.start_matlab()

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

    # Create MATLAB figure (only once)
    eng.figure('Visible', 'off', nargout=0)  

    # Plot Deputy's scatter plot (Blue)
    deputy_positions = matlab.double([deputyXpos, deputyYpos, deputyZpos])
    scatter_handle = eng.scatter3(*deputy_positions, 50, 'b', 'filled', nargout=1)

    # Set graph properties
    eng.eval("xlabel('X Values'); ylabel('Y Values'); zlabel('Z Values'); title('3D Live Graph'); grid on; hold on;", nargout=0)

    # Extract Chief positions
    chiefXpos = [row[0] for row in x]
    chiefYpos = [row[1] for row in x]
    chiefZpos = [row[2] for row in x]

    # Plot Chief's scatter plot (Red)
    chief_positions = matlab.double([chiefXpos, chiefYpos, chiefZpos])
    scatter_handle = eng.scatter3(*chief_positions, 50, 'r', 'filled', nargout=1)

    # Save the updated graph
    eng.saveas(eng.gcf(), IMAGE_PATH, 'png', nargout=0)
    elapsed = time.time() - curr
    print(f"Total elapsed time: {elapsed:.2f} seconds")

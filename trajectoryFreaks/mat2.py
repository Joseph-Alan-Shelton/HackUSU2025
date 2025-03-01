from trajectoryFreaks/models.py import best_fit_plane
# Start MATLAB Engine
eng = matlab.engine.start_matlab()

# Define image path
image_path = "static/images/graph.png"

# Initialize x, y, z values
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
z = [2, 4, 6, 8, 10]

best_fit_plan(x,y,z)
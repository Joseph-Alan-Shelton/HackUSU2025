from django.db import models
import matlab.engine

# Create your models here.
x = [1, 2, 3, 4, 5]
y = [10, 12, 15, 20, 25]

def findFit():
    eng = matlab.engine.start_matlab()

    # Call matlab script to find fit of points
    degreeOfFit = 6
    error, x_fit, y_fit = eng.leastSquareFit(x, y, degreeOfFit, nargout=3)

    eng.quit()
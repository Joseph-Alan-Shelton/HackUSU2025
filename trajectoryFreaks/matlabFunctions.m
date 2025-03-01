% Least Square Polynomial Fitting
% Takes in a x and y vector along with a degree to fit them to
% returns a x and y vector of specified degree along with the error 
function [error, x_fit, y_fit] = leastSquareFit(x, y, degreeOfFit)
    y = y'; % needs to be row vector not column
    numberOfPoints = length(x); % number of points
    plot_numberOfPoints = length(x); % number of points for plotting fit

    % Build a vandermonde matrix
    V = zeros(numberOfPoints, degreeOfFit+1);
    
    for row = 1:numberOfPoints
        v = x(row);
        V(row, 1) = 1.0;
        for col = 2:degreeOfFit+1
            V(row, col) = v^(col - 1);
        end
    end
    
    % Solve the normal equations
    AtA = V' * V; % left side matrix of the normal equation, A^T * A
    Aty = V' * y'; % right side of the normal equation A^T * y
    coeff = flip(AtA\Aty); % solution to the normal equation x = (A^T * A)^(-1) * A^T * y
    
    x_fit = linspace(min(y), max(y), plot_numberOfPoints); % plot space for the fit
    y_fit = polyval(coeff, x_fit); % evaluate the fit over the plot space
    
    % Calculate the least squares error
    error = norm(y-y_fit, 2) / norm(y);
end
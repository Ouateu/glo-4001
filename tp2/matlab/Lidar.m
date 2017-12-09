function [ X, Y ] = Lidar( coordX, coordY, omega, sigma, Carte )
%LIDAR Retourne une mesure de lidar dans la direction omega
%   Detailed explanation goes here
lineX = [coordX, coordX+20*cos(omega)];
lineY = [coordY, coordY+20*sin(omega)];
[xi, yi] = polyxpoly(lineX, lineY, Carte(1, :), Carte(2, :));

if isempty(xi) || isempty(yi)
    X = 0;
    Y = 0;
    return
end

closestIndex = ClosestMatch(coordX, coordY, xi, yi);
X = xi(closestIndex) + sigma*randn() - coordX;
Y = yi(closestIndex) + sigma*randn() - coordY;
end


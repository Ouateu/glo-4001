function [ Index ] = ClosestMatch( x, y, xi, yi )
%CLOSESTMATCH Retourne le match le plus proche
%   Detailed explanation goes here

Index = 0;
closest_distance = 100;
for i = 1:size(xi, 1)
    match_distance = sqrt((x - xi(i))^2 + (y - yi(i))^2);
    if match_distance < closest_distance
        closest_distance = match_distance;
        Index = i;
    end
end

end
function [intersections_x, intersections_y] = ClosestLidarIntersection(Carte, positionRobot, angleRobot, sigLidar)
    lidarDirection = [0, (pi/2), pi, ((3*pi)/2)];
    lidarDistanceMax = 20;
    intersections_x = [];
    intersections_y = [];
    for iDirection = 1:length(lidarDirection)
        x_line = [positionRobot(1), positionRobot(1) + lidarDistanceMax*cos(lidarDirection(iDirection)+angleRobot)];
        y_line = [positionRobot(2), positionRobot(2) + lidarDistanceMax*sin(lidarDirection(iDirection)+angleRobot)];
        
        [i_x, i_y] = polyxpoly(x_line, y_line, Carte(1, :), Carte(2,:));
        mesure_x = 0;
        mesure_y = 0;
        distance = inf;
        for i = 1:length(i_x)
            temp_distance = pdist([i_x(i), i_y(i); positionRobot(1), positionRobot(2)], 'euclidean');
            if(temp_distance < distance)
                mesure_x = i_x(i);
                mesure_y = i_y(i);
                distance = temp_distance;
            end
        end
        intersections_x = [intersections_x; mesure_x + normrnd(0, sigLidar)];
        intersections_y = [intersections_y; mesure_y + normrnd(0, sigLidar)];
    end
end
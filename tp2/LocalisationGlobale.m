clearvars
load('res/Carte.mat')

myFontSize = 14; % Taille de la police de caractere pour les graphes
nStep = 100;
dt = 0.1;
nParticules = 100;
Reff = 0.5;

lidarDirection = [0, (pi/2), pi, ((3*pi)/2)];
lidarDistanceMax = 20;
sigLidar = 0.01;
sigVitesse = 0.01;

vitesse = 0;
angleRobot = 0;
sigAngle = 0.01;
sigPositionEstime = 1;
sigVitesseEstime = sigVitesse*;

%x = rand(1, nParticules)*18;
%y = rand(1, nParticules)*8;

x = ones(1, nParticules);
y = 2*ones(1, nParticules);

Xvrai = [1; 2];
X = [x; y];

w = ones(1, nParticules)./nParticules;


X2Vrai = [];
X2Mesure = [];

for iStep = 1:nStep
    time = iStep*dt;
    angleCompas = angleRobot + sigAngle*randn;

    %%% Simulation des mesures %%%
    Xvrai(1) = Xvrai(1) + dt*(vitesse + sigVitesse*randn)*cos(angleCompas);
    Xvrai(2) = Xvrai(2) + dt*(vitesse + sigVitesse*randn)*sin(angleCompas);
    
    [intersections_x, intersections_y] = ClosestLidarIntersection(Carte, Xvrai, angleCompas, sigLidar);
        
    ligne1_x = [intersections_x(1), intersections_x(3)];
    ligne1_y = [intersections_y(1), intersections_y(3)];
    ligne2_x = [intersections_x(2), intersections_x(4)];
    ligne2_y = [intersections_y(2), intersections_y(4)];
    
    [Xmesure, Ymesure] = polyxpoly(ligne1_x, ligne1_y, ligne2_x, ligne2_y);
    
    
    %%% Filtre a particules
    for iParticule=1:nParticules
        X(1, iParticule) = X(1, iParticule) + dt*(vitesse + sigVitesseEstime*randn*10)*cos(angleCompas);
        X(2, iParticule) = X(2, iParticule) + dt*(vitesse + sigVitesseEstime*randn*10)*sin(angleCompas);
        wnew = 0;
        [estime_intersection_x, estime_intersection_y] = ClosestLidarIntersection(Carte, X(:, iParticule), angleCompas, sigLidarEstime);
        
        for iDirection = 1:length(lidarDirection)
            dis_x = estime_intersection_x(iDirection) - intersections_x(iDirection);
            dis_y = estime_intersection_y(iDirection) - intersections_y(iDirection);
            wnew = wnew*gauss(dis_x, sigLidarEstime);
            wnew = wnew*gauss(dis_y, sigLidarEstime);
        end
       display(wnew);
       
        w(iParticule) = w(iParticule)*wnew;
    end
    [X, w] = ParticuleResampling(X, w, Reff);
    
    %%% Dessin des données
    X2Vrai = [X2Vrai Xvrai];
    %X2Mesure = [X2Mesure [Xmesure; Ymesure]];
    clf
    h(1) = plot(Carte(1, :), Carte(2, :));
    hold on
    PlotParticules2D(X,angleRobot, w,'o',0.1);
    h(2) = plot(intersections_x', intersections_y', 'r*');
    h(3) = plot(Xvrai(1), Xvrai(2), 'k+');
    %h(5) = plot(X2Mesure(1, :), X2Mesure(2, :), 'go');
    hold off
    xlabel('Temps (s)');
    ylabel('Estime de position (m)');
    legend(h,{'Carte reel', 'lidar', 'position reel'});

    drawnow();
end
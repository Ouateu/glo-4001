clearvars
clf
load('../res/Carte.mat')

% Props du systeme
SLidar = 0.01;
SLinear = 0.01;
SAngular = 0.05;
SCompass = 0.01;

NSteps = 20;
dt = 0.1;

% Init du GT
XVrai = 2;
YVrai = 1;
OmegaVrai = pi/2;
linearSpeed = 1;
angularSpeed = deg2rad(-25);
lidarDirections = [0, pi/2, pi, 3*pi/2]; %offset de chacun des lidars
vraiLidars = zeros(2, 4);

% Init des particules
C = 100;
particules = zeros(4, 100);
lidars = zeros(2, 400);

% Mise en memoire de la trajectoire
trajectory = [];

for i = 1:C
    x = rand()*20;
    y = rand()*7;
    omega = OmegaVrai + SCompass*rand();
    particules(1, i) = x;
    particules(2, i) = y;
    particules(3, i) = omega;
    particules(4, i) = 1/C;
    for j = 1:length(lidarDirections)
        [xlidar, ylidar] = Lidar(x, y, omega+lidarDirections(j), SLidar, Carte);
        lidars(1, i+(j-1)*100) = xlidar;
        lidars(2, i+(j-1)*100) = ylidar;
    end
end

% Boucle de simulation
for step = 1:NSteps
    % Simulation GT
    speed = linearSpeed + SLinear*randn();
    XVrai = XVrai + speed * cos(OmegaVrai) * dt;
    YVrai = YVrai + speed * sin(OmegaVrai) * dt;
    OmegaVrai = OmegaVrai + (angularSpeed+  SAngular*randn()) * dt;
    for j = 1:length(lidarDirections)
        [XLidar, YLidar] = Lidar(XVrai, YVrai, OmegaVrai + lidarDirections(j), SLidar, Carte);
        vraiLidars(1, j) = XLidar;
        vraiLidars(2, j) = YLidar;
    end
    
    % Mise a jour des particules
    for i = 1:length(particules)
        x = particules(1, i);
        y = particules(2, i);
        omega = particules(3, i);
        speed = linearSpeed + SLinear*randn();
        particules(1, i) = x + speed * cos(omega) * dt;
        particules(2, i) = y + speed * sin(omega) * dt;
        particules(3, i) = omega + (angularSpeed + SAngular*randn()) * dt;
        for j = 1:length(lidarDirections)
            [xlidar, ylidar] = Lidar(x, y, omega+lidarDirections(j), SLidar, Carte);
            lidars(1, i+(j-1)*100) = xlidar;
            lidars(2, i+(j-1)*100) = ylidar;
        end
    end
    
    % Calcul des poids
    for i = 1:length(particules)
        wnew = particules(4, i);
       for j = 1:length(lidarDirections)
           xparticule = lidars(1, i+(j-1)*100);
           yparticule = lidars(2, i+(j-1)*100);
           xu = vraiLidars(1, j);
           yu = vraiLidars(2, j);
           wnew = gauss(xparticule, xu, 1) * wnew;
           wnew = gauss(yparticule, yu, 1) * wnew;
       end
       particules(4, i) = wnew;
    end
    
    % Resampling
    w = particules(4, :);
    wNorm = sum(w);
    w = w./wNorm;
    
    xWeight = 0
    yWeight = 0
    for i = 1:C
        xWeight = particules(1, i) * w(i) + xWeight;
        yWeight = particules(2, i) * w(i) + yWeight;
    end
    nextTrajectory = [xWeight; yWeight];
    trajectory = [trajectory nextTrajectory];
    
    Neff = 1/sum(w.^2);
    display(Neff)
    if Neff < 0.3*C
        display('Resampling')
        Copy = zeros(1, C);
        Q = cumsum(w);
        T = sort(rand(1, C+1));
        T(C+1) = 1;
        idx = 1;
        jdx = 1;
        while (idx <= C)
            if T(idx) < Q(jdx)
                Copy(idx) = jdx;
                idx = idx + 1;
            else
                jdx = jdx + 1;
            end
        end
        w = ones(1, C)./C;
        particules(4,:) = w;
        particules = particules(:,Copy);
        
    end
    
end
    % Affichage de la simulation
hold off
clf
hold on
plot(Carte(1, :), Carte(2, :), 'b-')
plot(XVrai, YVrai, 'ro')
plot(vraiLidars(1, :), vraiLidars(2, :), 'rx')
plot(particules(1, :), particules(2, :), 'go')
plot(trajectory(1, :), trajectory(2, :), 'r-')
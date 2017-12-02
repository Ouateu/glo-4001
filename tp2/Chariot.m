% Systeme representant le chariot pour le TP3, Automne 2015
% (c) Philippe Giguere, 2015 Version 1.0
clearvars
clf
myFontSize = 14; % Taille de la police de caractere pour les graphes

% Parametre du systeme
d_init  =    % Point de depart du robot
SAngle  =    % Écart-type du bruit sur la mesure d'angle.
SV      =    % Écart-type du bruit sur le voltage du moteur.
nStep   = 400;     % Nombres de mesures/pas
dT      = 0.1;     % Intervalle de temps entre les mesures/pas

% Important! Il faut initialiser la matrice X de facon a avoir
% une dimension (2,1) et non (1,2). Sinon, le filtre EKF ne marchera pas.
xVrai = [d_init 0]'; % Etat reel, inconnu du filtre et du robot.

% Specifier les valeurs initiales des matrices.
% Ne pas oublier qu'ici, ce sont des covariances, pas des ecarts-types.
X = [d_init 0]'; % un exemple d'initialisation.
P = 


for iStep = 1:nStep
    % Simulation du systeme a chaque etape
    time = iStep*dT;

    % Commande de voltage envoye vers le systeme.
    U = 8*sin(0.2*pi*time);

    % ============== Debut de la simulation du deplacement reel ===========   
    % Le deplacement veritable du chariot selon les equations.
    % Je vous donne les equations, vous n'avez rien a changer ici.

    xVrai(1) = xVrai(1) + (xVrai(2))*dT; % Calcul du deplacement
    xVrai(2) = 2.*(1/(1+exp(-0.5*(U+randn*SV)))-0.5);   % Calcul de la vitesse
    
    % Je simule pour vous la réponse de la caméra.
    % Le max(0.001,...) est pour éviter les valeurs négatives.
    z = max(0.001,0.07/xVrai(1) + SAngle*randn);
    % =============== Fin de la simulation de deplacement reel ============   

    % ================ Debut de votre filtre E K F ou particule ==================
    % ATTENTION ATTENTION ATTENTION ATTENTION
    % Vous n'avez pas le droit d'utiliser xVrai dans votre filtre
    % car c'est la position et la vitesse reele du systeme, et 
    % elles vous sont inconnues.

    Votre code ici!
    

    % ========= Fin des equations du filtre EKF ou particule =============
    
    % Cueillette des donnees pour les graphiques/statistiques
    AxVrai1(iStep)  = xVrai(1);
    AxVrai2(iStep)  = xVrai(2);
    AX1(iStep)      = X(1);
    AX2(iStep)      = X(2);
    AU(iStep)       = U;
    AZ(iStep)       = z;
    ATime(iStep) = time;
    
    % Pour voir votre filtre evoluer dans le temps
    clf
    h(1) = plot(ATime,AX1,'go');
    hold on;
    h(2) = plot(ATime,AxVrai1,'k-','LineWidth',2);
    h(3) = plot(ATime,0.07./AZ,'r*'); % Ici on peut inverser le capteur, pour trouver la position correspondant a z.
    xlabel('Temps (s)');
    ylabel('Estime de position (m)');
    legend(h,{'EKF','Position Exacte','Mesure h_z^{-1}'});
    ylim([0 20]);
    drawnow();
end

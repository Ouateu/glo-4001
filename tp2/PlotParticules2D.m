function h = PlotParticules2D(X,a,W,Symbol,LongeurFleche)
    % Tracer la position des particules, avec le heading
    hold on;   
    % Pour avoir une couleur en fonction du poids
    if (range(W)>0)
        WN = (W-min(W))/range(W);
    else
        WN = ones(1,size(W,2)); 
    end
    
    for iP = 1:size(X,2)
       xp = X(1,iP);
       yp = X(2,iP);
       h = plot(xp,yp,Symbol,'MarkerFaceColor',(1-WN(iP)).*[1 1 1]);
       line([xp  xp+LongeurFleche*cos(a)],[yp yp+LongeurFleche*sin(a)]);
       %hsv2rgb([WN(iP) 1 1]);
       % Tracer une ligne pour la direction
    end
end
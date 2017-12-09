function out = gauss(x, u,s)
    out = (1/sqrt(2*pi*s^2))*exp(-((x-u)/(2*s^2))^2);
end
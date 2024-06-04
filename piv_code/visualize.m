clc; clear; close all;

data = readtable("FMT_group05\Images\15deg_PIV_MP(32x32_50ov)_PostProc=unknown\B00001.dat", "NumHeaderLines", 3);
x_global = table2array(data(:, 1));
y_global = table2array(data(:, 2));
u_global = table2array(data(:, 3));
v_global = table2array(data(:, 4));

nx = find(x_global==x_global(1));
nx = nx(2);

ny = length(y_global)/(nx - 1);

x = zeros(ny, nx);
y = zeros(ny, nx);
u = zeros(ny, nx);
v = zeros(ny, nx);

vel_limit = 20;

for i=1:ny-1
    for j=1:nx
        x(i, j) = x_global(j + (nx-1)*(i-1));
        y(i, j) = y_global(j + (nx-1)*(i-1));
        u_local = u_global(j + (nx-1)*(i-1));
        v_local = v_global(j + (nx-1)*(i-1));
        if abs(u_local) > vel_limit
            u_local = 0;
        end
        if abs(v_local) > vel_limit
            v_local = 0;
        end
        u(i, j) = u_local;
        v(i, j) = v_local;
    end
end

% levels = linspace(0, 30, 100);
colormap("hot");
contourf(x, y, sqrt(u.^2 + v.^2), "LineStyle", "none")
hold on 
quiver(x,y, u, v, "Color","green")
hold off
colorbar()
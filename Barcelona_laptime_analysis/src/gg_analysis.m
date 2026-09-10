accelData = readtable("BARCELONA.csv")

Long_A = accelData.CAR_G_AX
Lat_A = accelData.CAR_G_AY

scatter(Lat_A, Long_A, 8, 'filled')
ylabel("Longitudinal Acceleration /g")
xlabel("Lateral Acceleration /g")


accel_L = (Lat_A < -0.4) & (Long_A > 0.3);
accel_Pure = (abs(Lat_A) <= 0.4) & (Long_A > 0.3);
accel_R = (Lat_A > 0.4) & (Long_A > 0.3);
pure_L = (Lat_A < -0.4) & (abs(Long_A) <= 0.3 );
pure_R = (Lat_A > 0.4) & (abs(Long_A) <= 0.3 );
brake_L = (Lat_A < -0.4) & (Long_A < -0.3);
brake_R = (Lat_A > 0.4) & (Long_A < -0.3);
brake_Pure = (abs(Lat_A) <= 0.4) & (Long_A < -0.3);

% The remaining points 
centre = ~(accel_L | accel_Pure | accel_R | pure_L | pure_R | brake_L | brake_R | brake_Pure);

brightpurple = hex2rgb('#8A2BE2');
pink = hex2rgb('#FF1493');

figure;
hold on;
% Plot centre points first
scatter(Lat_A(mask_base), Long_A(mask_base), 6, [1 1 1], 'filled', 'DisplayName', 'Centre'); 
grid on
% Overlay the highlighted regions 
scatter(Lat_A(accel_L), Long_A(accel_L), 6, [1 0.549 0], 'filled', 'DisplayName', 'Left Acceleration');
scatter(Lat_A(accel_Pure), Long_A(accel_Pure), 6, 'yellow', 'filled', 'DisplayName', 'Pure Acceleration');
scatter(Lat_A(accel_R), Long_A(accel_R), 6, 'g', 'filled', 'DisplayName', 'Right Acceleration');
scatter(Lat_A(pure_R), Long_A(pure_R), 6, 'cyan', 'filled', 'DisplayName', ' Pure Right Cornering');
scatter(Lat_A(pure_L), Long_A(pure_L), 6, 'r', 'filled', 'DisplayName', ' Pure Left Cornering');
scatter(Lat_A(brake_R), Long_A(brake_R), 6, 'b', 'filled', 'DisplayName', 'Right Braking');
scatter(Lat_A(brake_L), Long_A(brake_L), 6, 'magenta', 'filled', 'DisplayName', 'Left Braking');
scatter(Lat_A(brake_Pure), Long_A(brake_Pure), 6, [0.5412 0.1686 0.8863], 'filled', 'DisplayName', 'Pure Braking')

hold off;

ylabel("Longitudinal Acceleration /g")
xlabel("Lateral Acceleration /g")
title("G-G Diagram")
legend();

totalPoints = height(accelData)

region = strings(size(Long_A));

region(accel_L) = "Left Acceleration";
region(accel_Pure) = "Pure Acceleration";
region(accel_R) = "Right Acceleration";
region(pure_L) = "Pure Left Cornering";
region(pure_R) = "Pure Right Cornering";
region(brake_L) = "Left Braking";
region(brake_R) = "Right Braking";
region(brake_Pure) = "Pure Braking";
region(centre) = "Centre";

region = categorical(region);

regions = categories(region);
counts = groupcounts(region);
percentages = (counts ./ totalPoints)*100;

T = table(regions, percentages)
colours = [
    1     1     1
    1     0.549 0
    1     0     1
    1     1     0
    0.541 0.169 0.8863
    1     0     0
    0     1     1
    0     1     0
    0     0     1 ]

[percentages_sorted, idx] = sort(percentages, 'descend');
regions_sorted = regions(idx);
colours_sorted = colours(idx, :);

figure;

b = barh(percentages_sorted, 'FaceColor', 'flat');
b.CData = colours_sorted;

yticklabels(regions_sorted)
xlabel('Percentage of Samples (%)')
title('% of laptime in each region')
grid on

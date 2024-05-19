clc; clear all; close all;

I = imread("PIV Samples\15deg\B00001.tif");
I = im2double(I);
sizeI = size(I);

image1 = I(1:sizeI(1)/2,:);
image2 = I(sizeI(1)/2+1:end,:);

image1 = imgaussfilt(image1, 5);
image2 = imgaussfilt(image2, 5);

% image1 = image1 - mean(image1(:));
% image2 = image2 - mean(image2(:));

windowSize = 16; % Size of the interrogation window
step = windowSize; % Step size for window overlap

% Preallocate vectors for displacement
[rows, cols] = size(image1);
u = zeros(round(rows/step), round(cols/step)); % Horizontal displacement (u-component of velocity)
v = zeros(round(rows/step), round(cols/step)); % Vertical displacement (v-component of velocity)

% Loop over each interrogation window
rowRange = 1:step:(rows-windowSize);
colRange = 1:step:(cols-windowSize);
jump = windowSize-1;
for i = rowRange
    for j = colRange
        % Extract the interrogation windows
%         if i == 1
%             if j == 1
%                 subImage1 = image1(i:i+2*jump, j:j+2*jump);
%             elseif j == max(colRange)
%                 subImage1 = image1(i:i+2*jump, j-jump:j+jump);
%             else
%                 subImage1 = image1(i:i+2*jump, j-jump:j+2*jump);
%             end
%         elseif i == max(rowRange)
%             if j == 1
%                 subImage1 = image1(i-jump:i+jump, j:j+2*jump);
%             elseif j == max(colRange)
%                 subImage1 = image1(i-jump:i+jump, j-jump:j+jump);
%             else
%                 subImage1 = image1(i-jump:i+jump, j-jump:j+2*jump);
%             end
%         elseif j == 1
%             subImage1 = image1(i-jump:i+2*jump, j:j+2*jump);
%         elseif j == max(colRange)
%             subImage1 = image1(i-jump:i+2*jump, j-jump:j+jump);
% %         else
% %             subImage1 = image1(i-2*jump:i+2*jump, j-2*jump:j+2*jump);
%         end
%         subImage1 = image1;

        subImage1 = image1(i:i+windowSize-1, j:j+windowSize-1);
        subImage1 = subImage1 - mean(subImage1);

        subImage2 = image2(i:i+windowSize-1, j:j+windowSize-1);
        subImage2 = subImage2 - mean(subImage2);

        % Cross-correlation
        correlation = xcorr2(subImage1,subImage2);
        
        % Find the peak in the correlation matrix
        [~, maxIndex] = max(correlation(:));
        [peakRow, peakCol] = ind2sub(size(correlation), maxIndex);

        % Calculate displacement
        u((i-1)/step+1, (j-1)/step+1) = peakCol;
        v((i-1)/step+1, (j-1)/step+1) = peakRow;
        [i j]
    end
end

timeInterval = 0.0001; % Time between frames in seconds
scalingFactor = 0.001; % Meters per pixel

velocityX = u; %* scalingFactor / timeInterval;
velocityY = v; %* scalingFactor / timeInterval;
totalVelocity = sqrt(velocityX.^2 + velocityY.^2);
% [X, Y] = meshgrid(1:step:cols, 1:step:rows);
% quiver(velocityX, velocityY);
contourf(velocityX,"LineStyle","none")
% colorbar
% %%
% figure
% % velocityX(20,13) = NaN;
% % velocityX(18,13) = NaN;
% totalVelocity(:,end) = NaN;
% totalVelocity(end,:) = NaN;
% contourf(totalVelocity,"LineStyle","none")
% % caxis([10, 30])
% colormap parula
% colorbar

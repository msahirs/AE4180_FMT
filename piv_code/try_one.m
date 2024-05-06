%XCORR2_FFT Two-dimensional cross-correlation evaluated with FFT algorithm.
%   XCORR2_FFT(A,B) computes the cross-correlation of matrices A and B.
%   XCORR2(A) is the autocorrelation function.
%   
%   When matrices A and B are real, XCORR2_FFT is numerically equivalent to
%   XCORR2 but much faster.
%
%   % Example:
  a = rand(122); b=rand(332);
  a = a-mean(a(:));
  b = b-mean(b(:));

  tic,cl = xcorr2(a,b);toc
  % Elapsed time is 0.223502 seconds.
  tic,cf = xcorr2_fft(a,b);toc
  % Elapsed time is 0.030935 seconds.

  max(abs(cf(:)-cl(:)))
%   ans = 4.1922e-13
%
%   Author: Alessandro Masullo, 2015
%   Version 1.2
%
%   See also CONV2, XCORR, XCORR2 and FILTER2.
from math import *

#old guassian belief of position
mean1 = 10.
variance1 = 8.
#guassian measurement
mean2 = 13.
variance2 = 2.

#calculating new belief of position

mean3 = 1./(variance1+variance2)*(variance2*mean1+variance1*mean2)
variance3 = 1./(1./variance1+1./variance2)

print mean3, variance3

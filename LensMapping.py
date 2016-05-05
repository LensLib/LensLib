# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:30:31 2016

@author: Guido Davoli
"""

import numpy
from astropy.io import fits

  
class Lens:
    
    #ALL LENGHTS ARE EXPRESSED IN ADIMENSIONAL NOTATION
    
    def __init__(self, angle_x_map, angle_y_map): #angles maps must be two strings telling the path to the fits files representing the deflection angle maps
        
        hdulist_x = fits.open(angle_x_map) #opening fit deflection maps
        hdulist_y = fits.open(angle_y_map)#hdulist is a list of Header/Data Units (HDU), the "building block" of fits files

        self.deflection_x = hdulist_x[0].data #we expect to find deflection maps in the primary (0th) HDU  
        self.deflection_y = hdulist_y[0].data #deflection_x&y are 2-dimensional arrays containing numerical values of pixels of the fits images

    def convergence_map(self): #return the value of the convergence at the point (x1,x2) on the lens plane
        
        gradient_x=numpy.gradient(self.deflection_x)#gradient_x is a list of two arrays corresponding to the maps of the two component of the gradient of the x component of the deflection angles
        gradient_y=numpy.gradient(self.deflection_y)
        
        #I'm looking for the divergence of the deflection angle: I get it adding the
        #x component of the gradient of the x component of the angle to the y component
        #of the gradient of the y component of the angle. Dividing by two I obtain the 
        #convergence:
        
        convergence=0.5*(gradient_x[0] + gradient_y[1]) #convergence is a 2d array, representing a map. LACKING THE FACTOR (einstein_rad/D_L)^2!!!!!!!!!!!!!!!!
    
        return convergence #convergence is a 2d array which dimension is is that of the deflection maps

        
    
        
        
        
        
        
        
  

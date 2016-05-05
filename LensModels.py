# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:41:43 2016

@author: Guido Davoli

"""

import numpy

class PowerLawLens:
    
    #ALL LENGHTS ARE EXPRESSED IN ADIMENSIONAL NOTATION 
    #(DIVIDED BY THE EINSTEIN RADIUS)

    def __init__(self,index):
        
        self.n=index #power law index n
        
        #this is the constructor of the class PowerLawLens
	
    def deflection_angle(self,x1,x2):

        module=(numpy.sqrt((x1**2 + x2**2)))**(2-self.n) #module of the deflection angle at the point (x1,x2) for a power-law lens  
        x1_component=module*x1/numpy.sqrt(x1**2+x2**2) #the deflection angle vector point always away from the lens center
        x2_component=module*x2/numpy.sqrt(x1**2+x2**2)
        angle=[x1_component,x2_component]        
        
        return angle
                  
        #This function return an array called angle that describes the
        #deflection angle at the point (x1,x2) on the lens plane

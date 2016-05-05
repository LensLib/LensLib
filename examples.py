# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:50:17 2016

@author: Guido Davoli

"""
########## HOW TO USE LensMapping.py AND LensModels.py: SOME EXAMPLES #########

import LensModels
import LensMapping
import numpy
from astropy.io import fits

lens=LensModels.PowerLawLens(4) #lens a PowerLawLens with index n=4
angle_x1comp_map=numpy.zeros([500,500]) # 500x500 array filled with zeros
angle_x2comp_map=numpy.zeros([500,500]) 
for x1 in range (500):
    for x2 in range (500): 
        angle=lens.deflection_angle((x1-250)/500,(x2-250)/500) #angle is an array containing the two components of the deflection angle at the point (x1,x2)
        angle_x1comp_map[x1,x2]=angle[0] #filling the maps of the deflection angle
        angle_x2comp_map[x1,x2]=angle[1]

hdu = fits.PrimaryHDU(angle_x1comp_map) #HDU means Header/Data Unit, the 'building blocks' of which fit files are made of. In this case, hdu is a pure data unit.
hdu.writeto('data/angle_x1comp_map.fits') #the HDU hdu is written to the new fit file. A simple header is automatically attached to the file.

hdu = fits.PrimaryHDU(angle_x2comp_map) 
hdu.writeto('data/angle_x2comp_map.fits') 

hdulist_x1 = fits.open('data/angle_x1comp_map.fits') #opening fits deflection maps
hdulist_x2 = fits.open('data/angle_x2comp_map.fits')#hdulist is a list of Header/Data Units

lens2=LensMapping.Lens('data/angle_x1comp_map.fits','data/angle_x2comp_map.fits')
convergence=lens2.convergence_map()

hdu = fits.PrimaryHDU(convergence) 
hdu.writeto('data/convergence.fits') 
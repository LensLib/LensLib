#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
from astropy import constants as const
from astropy import units as u


class Microlens:
	

	def __init__(self, M, D_l, D_s, beta):
		"""
		Questo è il costruttore della classe Microlens.
		Prende gli attributi dati in input e se ne
		aggiunge anche di nuovi, definibili con
		i metodi della classe sottostanti.
		"""
		self.M = M.to(u.kg)
		self.D_l = D_l.to(u.m)
		self.D_s = D_s.to(u.m)
		self.beta = beta.to(u.rad)
		self.thetaE = self.einstein_rad()
		self.y = self.beta/self.thetaE


	def einstein_rad (self):
		"""
		Calcola il raggio di Einstein in radianti
		Si assume che D_s = D_l + D_ls.
		G e c sono prese dal modulo constants di astropy.
		dist è una dummy variable per semplificare il codice.
		L'angolo risultante è in radianti, quindi lo si
		esplicita con il modulo units di astropy.
		"""
		G = const.G
		c = const.c
		D_ls = self.D_s - self.D_l
		dist = D_ls/(self.D_s*self.D_l)
		theta = np.sqrt(4.*G*self.M*dist/c**2)
		return (theta*u.rad)


	def image_pos (self):
		"""
		Dà la distanza dell'immagine (x_i) e 
		della controimmagine (x_c) rispetto alla
		lente, disposte lungo una retta che collega
		lente e sorgente. L'output è la lista x
		che contiene x_i e x_c.
		"""
		y = self.y
		x_i = 0.5*(y + np.sqrt(y**2 + 4.))
		x_c = 0.5*(y - np.sqrt(y**2 + 4.))
		x = [x_i, x_c]
		return (x)


	def magnification (self):
		"""
		Calcola l'amplificazione di immagine (m_i)
		e controimmagine (m_c) che si formano
		con un evento di microlensing. L'output
		è la lista mu che contiene m_i e m_c.
		"""
		y = self.y
		m_i = 0.5*(1. + (y**2 + 2.)/(y*np.sqrt(y**2+4.)))
		m_c = 0.5*(1. - (y**2 + 2.)/(y*np.sqrt(y**2+4.)))
		mu = [m_i, m_c, np.absolute(m_i) + np.absolute(m_c)]
		return (mu)


	def centroid_shift (self):
		"""
		Calcola il centroid shift in unità adimensionali
		"""
		y = self.y
		x_c = y*(y**2 + 3)/(y**2 + 2)
		return (x_c)


	def deviation (self):
		"""
		Calcola la deviazione del baricentro della luce: 
		delta = y - x_c
		"""
		y = self.y
		delta = y/(y**2 + 2)
		return(delta)



# Esempio dati input

M = 1.*u.solMass
D_l = 4e3*u.pc
D_s = 8.e3*u.pc
beta = 1.e-1*u.mas


# star è un'istanza della classe Microlens

star = Microlens (M, D_l, D_s, beta)


# Output dei dati prodotti dai metodi della classe

print "Einstein radius"
print star.thetaE.to(u.mas)

print "Image position (in Einstein radii)"
print star.image_pos()[0]
print "Counterimage position (in Einstein radii)"
print star.image_pos()[1]

print "Total magnification"
print star.magnification()[2]

print "Centroid shift (in Einstein radii)"
print star.centroid_shift()

print "Deviation (in Einstein radii)"
print star.deviation()
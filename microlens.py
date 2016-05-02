#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as pl
from pylab import *
ion()
from astropy import constants as const
from astropy import units as u


class Microlens:
	

	def __init__(self, M, D_l, D_s, beta_0, v, t):
		"""
		Questo è il costruttore della classe Microlens.
		Prende gli attributi dati in input e se ne
		aggiunge anche di nuovi, definibili con
		i metodi della classe sottostanti.
		Le unità di misura usate sono le MKS.
		"""
		self.M = M.to(u.kg)
		self.D_l = D_l.to(u.m)
		self.D_s = D_s.to(u.m)
		self.beta_0 = beta_0.to(u.rad)
		self.v = v.to(u.m/u.s)
		self.t = t
		self.thetaE = self.einstein_rad()
		self.t_E = self.einstein_time()
		self.beta = self.photo_lensing()
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
		return (delta)


	def einstein_time (self):
		"""
		Definisce il tempo scala t_E
		come il tempo che impiega a passare
		entro un raggio di Einstein la 
		sorgente dietro la lente.
		"""
		thetaE = np.tan(self.thetaE)
		t_E = thetaE*self.D_l/self.v
		return (t_E)


	def photo_lensing (self):
		"""
		Calcola un vettore di amplificazione
		in funzione del tempo, a seconda
		della velocità relativa tra lente e sorgente.
		"""
		beta_0 = self.beta_0
		thetaE = self.thetaE
		delta_t = (self.t/self.t_E)
		beta = np.sqrt(beta_0**2 + (thetaE*delta_t)**2)
		return (beta)


	def plot_magnification (self):
		"""
		Plotta l'amplificazione totale della sorgente
		in funzione del tempo in anni.
		"""
		t = self.t.to(u.yr)
		mu = self.magnification()[2]
		plt.figure ()
		plt.plot (t, mu, '-')
		plt.xlabel ("t [yr]",fontsize=15) 
		plt.ylabel ("$\mu$",fontsize=15)
		raw_input ("Press enter to continue")
		plt.close ()


	def plot_images (self):
		"""
		Plotta la distanza di sorgente, immagine
		e controimmagine in funzione del tempo
		ed in unità adimensionali (cioè in unità
		del raggio di Einstein).
		"""

		t = self.t.to(u.yr)
		x_i = self.image_pos()[0]
		x_c = self.image_pos()[1]
		y = self.y

		plt.figure ()
		plt.scatter (t, x_i, c=t)
		plt.scatter (t, x_c, c=t)
		plt.scatter (t, y, c=t)
		plt.axhline (y=0.)
		plt.xlabel ("t [yr]",fontsize=15) 
		plt.ylabel ("x [$\\theta_E$]",fontsize=15)
		raw_input ("Press enter to continue")
		plt.close ()


	def plot_distances (self):
		"""
		Plotta la distanza di sorgente, immagine
		e controimmagine in funzione del tempo
		in unità angolari.
		"""

		t = self.t.to(u.yr)
		x_i = self.image_pos()[0]*self.thetaE*1.e3
		x_c = self.image_pos()[1]*self.thetaE*1.e3
		y = self.y*self.thetaE*1.e3

		plt.figure ()
		plt.scatter (t, x_i, c=t)
		plt.scatter (t, x_c, c=t)
		plt.scatter (t, y, c=t)
		plt.axhline (y=0.)
		plt.xlabel ("t [yr]",fontsize=15) 
		plt.ylabel ("$\\theta$ [$\mu$as]",fontsize=15)
		raw_input ("Press enter to continue")
		plt.close ()




# Esempio dati input
M = 10.*u.solMass
D_l = 4.e3*u.pc
D_s = 8.e3*u.pc
beta_0 = 1.e-1*u.mas
v = 200.*u.km/u.s
t = np.linspace(-1.e7, 1.e7, 1.e2)*u.s

# Variabili di controllo
print_data = False
plot_magnification = False
plot_images = False
plot_distances = True


# star è un'istanza della classe Microlens

star = Microlens (M, D_l, D_s, beta_0, v, t)


# Output dei dati prodotti dai metodi della classe

if print_data == True:
	print "Einstein radius"
	print star.thetaE.to(u.mas)
	print
	print "Image position (in Einstein radii)"
	print star.image_pos()[0]
	print "Counterimage position (in Einstein radii)"
	print star.image_pos()[1]
	print
	print "Total magnification"
	print star.magnification()[2]
	print
	print "Centroid shift (in Einstein radii)"
	print star.centroid_shift()
	print
	print "Deviation (in Einstein radii)"
	print star.deviation()
	print
	print "Einstein time"
	print star.einstein_time()
	print
	print "Beta(t)"
	print star.photo_lensing().to(u.mas)


# Plot

if plot_magnification == True:
	star.plot_magnification()

if plot_images == True:
	star.plot_images()
	
if plot_distances == True:
	star.plot_distances()






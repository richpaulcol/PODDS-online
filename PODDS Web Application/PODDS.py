from flask import Flask,render_template,request


#import sqlite3
import pyhyd
import flask

import pylab as pp
import mpld3 as mp
import numpy as np


app = Flask(__name__)


fig,axs = pp.subplots(2,1,sharex=True)

@app.route('/')
def welcome():
	flask.url_for('static', filename='style.css')
	return render_template('PODDS.html')
	
#@app.route('/test')
#def test():
#	return "Dave"

@app.route('/inputs')
def plotting():
#	fig,axs = pp.subplots(2,1,sharex=True)
	#print request.args['arg1']
	Q_flush = np.float(request.args['Q_flush'])	## Getting the requests from the html server
	Q_flush = Q_flush/1000.				
	Q_0 = np.float(request.args['Q_0'])
	Q_0 = Q_0/1000.
	D = np.float(request.args['D'])
	L = np.float(request.args['L'])
	k_s = np.float(request.args['k_s'])
#	print "Dave"
	
		
	#####  Undertaking simple scaling calcs
	A = D**2 * np.pi/4	#Calc area
	V = Q_flush / A		#Calc pipe velocity
	TurnOver = int(L/V)	#Calc pipe turnover time
	
	
	maxt = 3*TurnOver		#Maximum simulation time is 3 times Turnover time
	dt =TurnOver/1000.		#time step is 0.001 turnover time  (this can be decreased for greater accuracy)
	t = np.arange(0,maxt,dt)	#the time range

	##### Shear stresses
	tau_s_0 = pyhyd.shear_stress(D, Q_0, k_s,)  	## Initial condition shear
	tau_a = pyhyd.shear_stress(D, Q_flush, k_s,)	## Applied shear

	### PODDS / VCDM Parameters
	alpha = 5	
	beta = 0.005
	
	### Output condition shear vector
	tau_s = np.zeros(t.size)
	tau_s[0] = tau_s_0
	#Output change in pipe wall material vector
	dN = np.zeros(t.size)
	#Output pipe turbidity vector
	T = np.zeros(t.size)
	#Ouput end of pipe turbidity vector
	Tend = np.zeros(t.size)
	
	dtau = (tau_a - tau_s_0) / 100.
	Shears = np.linspace(tau_s_0,tau_a+dtau,dtau)
	
	# Calculation of the change in shear stress over time
	for i in range(1,t.size):
		tau_s[i] = tau_s[i-1] + dt * beta*(tau_a - tau_s[i-1])
		
		dN[i] = alpha* beta*(tau_a - tau_s[i-1])
		T[i] = (4/D)*dN[i]
		
	#Calcualtion of the end of pipe shear stress
	#Integration of the Turbidity function
	Tend = np.cumsum(T)*dt
	#Tend2 is the decreasing turbidity function after turnover
	Tend2 = np.zeros(t.size)
	#calcualation of the falling limb of the turbidity function
	Tend2[int(TurnOver/dt):] = Tend[:int(t.size-TurnOver/dt)]
	
	#Adding the 
	Tend -= Tend2
	
	
	
	axs[0].plot(t,tau_s)#, 'ks-', mec='w', mew=5, ms=20)
	
	axs[0].set_ylabel('Condition Shear (Pa)' )
	axs[0].plot([TurnOver,TurnOver],[0,np.max(tau_s)],'k:',alpha = 0.5)
	
	axs[1].plot(t,Tend)
	axs[1].plot([TurnOver,TurnOver],[0,np.max(Tend)],'k:',alpha = 0.5)
	axs[1].plot([0,maxt],[np.max(Tend),np.max(Tend)],'k:',alpha = 0.5)
	axs[1].set_ylabel('Turbidity (TPMU)')
	axs[1].set_xlabel('Time (s)')
	axs[1].set_xlim(0,maxt)
	axs[1].set_ylim(0,np.max(Tend)*1.1)
	
	mp.save_html(fig,'templates/Sample.html')
	return mp.fig_to_html(fig)
	
@app.route('/clear')
def clear():
	axs[0].cla()
	axs[1].cla()
	return mp.fig_to_html(fig)

	

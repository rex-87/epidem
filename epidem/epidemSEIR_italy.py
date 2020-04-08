# -*- coding: utf-8 -*-
"""
	Epidem
	
	This project is an example of a Python project generated from cookiecutter-python.
"""

## -------- COMMAND LINE ARGUMENTS ---------------------------
## https://docs.python.org/3.7/howto/argparse.html
import argparse
CmdLineArgParser = argparse.ArgumentParser()
CmdLineArgParser.add_argument(
	"-v",
	"--verbose",
	help = "display debug messages in console",
	action = "store_true",
)
CmdLineArgs = CmdLineArgParser.parse_args()

## -------- LOGGING INITIALISATION ---------------------------
import misc
misc.MyLoggersObj.SetConsoleVerbosity(ConsoleVerbosity = {True : "DEBUG", False : "INFO"}[CmdLineArgs.verbose])
LOG, handle_retval_and_log = misc.CreateLogger(__name__)

try:
	
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.widgets import Slider, Button, RadioButtons
	
	# population size
	N = 1e6

	t_size = 1000
	tt = np.array(range(t_size))

	italy_cases = [
		1.0,
		2.6,
		3.8,
		5.3,
		7.5,
		10.8,
		14.7,
		18.6,
		28.0,
		33.7,
		41.4,
		51.1,
		63.8,
		76.6,
		97.2,
		121.9,
		151.6,
		167.8,
		206.0,
		206.0,
		291.9,
		349.7,
		409.0,
		462.5,
		520.8,
		590.3,
		678.3,
		777.2,
		885.6,
		977.5,
		1056.6,
		1143.4,
		1229.5,
		1332.0,
		1429.7,
		1528.5,
		1614.7,
		1681.6,
		1748.6,
		1827.7,
		1904.8,
		1980.6,
		2060.0,
		2131.4,
		2190.9,
		2241.1,
	]
	italy_cases += int(t_size - len(italy_cases))*[0]

	italy_deaths = [
		0.03,
		0.05,
		0.12,
		0.17,
		0.20,
		0.28,
		0.35,
		0.48,
		0.56,
		0.86,
		1.31,
		1.77,
		2.45,
		3.26,
		3.85,
		6.05,
		7.65,
		10.43,
		13.67,
		13.67,
		20.93,
		23.82,
		29.90,
		35.67,
		41.37,
		49.22,
		56.28,
		66.64,
		79.75,
		90.51,
		100.45,
		112.73,
		124.02,
		135.79,
		150.98,
		165.67,
		178.17,
		191.59,
		205.42,
		217.44,
		230.00,
		242.66,
		253.92,
		262.60,
		273.11,
		283.09,
	]
	italy_deaths += int(t_size - len(italy_deaths))*[0]

	D = np.zeros_like(tt, dtype = np.float); D[0] = 0.1
	E = np.zeros_like(tt, dtype = np.float); E[0] = 2
	I = np.zeros_like(tt, dtype = np.float); I[0] = 1
	R = np.zeros_like(tt, dtype = np.float); R[0] = 0
	S = np.zeros_like(tt, dtype = np.float); S[0] = N - D[0] - E[0] - I[0] - R[0]

	def update(val):
		hi_t = s_hi_t.val
		K_SE = s_K_SE.val
		K_EI = s_K_EI.val
		K_ID = s_K_ID.val
		K_IR = s_K_IR.val	
		K_RS = s_K_RS.val	
		
		K_SE_ = K_SE
		L = 16*[1]+7*[.5]+7*[.2]+7*[.1]+(t_size-26-7)*[.05]
		for t in tt[:-1]:
			# S >>> E >>> I >>> R >>> S
			#             I >>> D
			K_SE = K_SE_*L[t]
			
			dS = -K_SE*S[t]*I[t]/N + K_RS*R[t] 
			dE = K_SE*S[t]*I[t]/N - K_EI*E[t]
			dI = K_EI*E[t] - K_IR*I[t] - K_ID*I[t]
			dR = K_IR*I[t] - K_RS*R[t]
			dD = K_ID*I[t]
			
			S[t+1] = S[t] + dS
			E[t+1] = E[t] + dE
			I[t+1] = I[t] + dI
			R[t+1] = R[t] + dR
			D[t+1] = D[t] + dD
		
		l_E.set_ydata(E)
		l_I.set_ydata(I)
		l_R.set_ydata(R)
		l_D.set_ydata(D)
		l_S.set_ydata(S)
		l_C.set_ydata(I+R)
		
		main_ax.set_xlim([0, hi_t])
		
		fig.canvas.draw_idle()
	
	fig, ax = plt.subplots(num="Modèle SIR(D)")
	plt.subplots_adjust(left = 0.08, bottom = 0.30, top = 0.92, right = 0.95)
	
	# plot_f = plt.plot
	plot_f = plt.semilogy
	l_S, = plot_f(tt, S, label='Susceptibles', color='blue')
	l_E, = plot_f(tt, E, label='Exposés'     , color='pink')
	l_I, = plot_f(tt, I, label='Infectés'    , color='red')
	l_R, = plot_f(tt, R, label='Rétablis'    , color='green')
	l_D, = plot_f(tt, D, label='Morts'       , color='black')
	l_C, = plot_f(tt, I+R,label='Confirmés'  , color='purple')
	l_italy_cases,  = plot_f(tt, italy_cases, '.', label='Italy', color='purple')
	l_italy_deaths, = plot_f(tt, italy_deaths, '.', label='Italy', color='black')
	
	main_ax = plt.gca()
	main_ax.set_xlim([0, 400])
	main_ax.set_ylim([1, N])
	plt.legend()
	plt.title('Modèle SEIR(D) - Italy Population [per million]')
	
	axcolor = 'lightgoldenrodyellow'	
	ax_hi_t = plt.axes([0.30, 0.22, 0.55, 0.03], facecolor=axcolor)
	ax_K_SE = plt.axes([0.30, 0.17, 0.55, 0.03], facecolor=axcolor)
	ax_K_EI = plt.axes([0.30, 0.13, 0.55, 0.03], facecolor=axcolor)
	ax_K_IR = plt.axes([0.30, 0.09, 0.55, 0.03], facecolor=axcolor)
	ax_K_ID = plt.axes([0.30, 0.05, 0.55, 0.03], facecolor=axcolor)
	ax_K_RS = plt.axes([0.30, 0.01, 0.55, 0.03], facecolor=axcolor)
	
	s_hi_t = Slider(ax_hi_t, 'Ajustement du temps'      , 1, t_size, valinit = 400  , valfmt='%d', valstep = 1)
	s_K_SE = Slider(ax_K_SE, 'Susceptibles -> Exposés ' , 0, 5.00, valinit = 1.31, valfmt='%1.4f')
	s_K_EI = Slider(ax_K_EI, 'Exposés -> Infectés'      , 0, 0.5, valinit = 0.18, valfmt='%1.4f')
	s_K_IR = Slider(ax_K_IR, 'Infectés -> Rétablis'     , 0, 0.5, valinit = 0.12, valfmt='%1.4f')
	s_K_ID = Slider(ax_K_ID, 'Infectés -> Morts'        , 0, 0.05, valinit = 0.018, valfmt='%1.4f')
	s_K_RS = Slider(ax_K_RS, 'Rétablis -> Susceptibles' , 0, 0.01, valinit = 0.000, valfmt='%1.4f')
	
	update(0)
	
	s_hi_t.on_changed(update)
	s_K_ID.on_changed(update)
	s_K_SE.on_changed(update)
	s_K_EI.on_changed(update)
	s_K_IR.on_changed(update)
	s_K_RS.on_changed(update)
	
	resetax = plt.axes([0.01, 0.95, 0.3, 0.04])
	button = Button(resetax, 'Réinitialiser les curseurs', color=axcolor, hovercolor='0.8')

	def reset(event):
		s_hi_t.reset()
		s_K_ID.reset()
		s_K_SE.reset()
		s_K_EI.reset()
		s_K_IR.reset()
		s_K_RS.reset()

	button.on_clicked(reset)
	
	plt.show()

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	input("Press any key to exit ...")

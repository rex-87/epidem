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
	
	t_size = 1000
	tt = np.array(range(t_size))
	
	# population size
	N = 100

	D = np.zeros_like(tt, dtype = np.float); D[0] = 0
	I = np.zeros_like(tt, dtype = np.float); I[0] = 0.1
	R = np.zeros_like(tt, dtype = np.float); R[0] = 0
	S = np.zeros_like(tt, dtype = np.float); S[0] = N - D[0] - I[0] - R[0]

	def update(val):
		hi_t = s_hi_t.val
		K_ID = s_K_ID.val
		K_SI = s_K_SI.val
		K_IR = s_K_IR.val	
		K_RS = s_K_RS.val	
		
		for t in tt[:-1]:
			
			# S >>> I >>> R >>> S
			#       I >>> D
			
			dS = -K_SI*S[t]*I[t]/N + K_RS*R[t] 
			dI = K_SI*S[t]*I[t]/N - K_IR*I[t] - K_ID*I[t]
			dR = K_IR*I[t] - K_RS*R[t]
			dD = K_ID*I[t]
			
			S[t+1] = S[t] + dS
			I[t+1] = I[t] + dI
			R[t+1] = R[t] + dR
			D[t+1] = D[t] + dD
		
		l_I.set_ydata(I)
		l_R.set_ydata(R)
		l_D.set_ydata(D)
		l_S.set_ydata(S)
		
		main_ax.set_xlim([0, hi_t])
		
		fig.canvas.draw_idle()
	
	fig, ax = plt.subplots(num="Modèle SIR(D)")
	plt.subplots_adjust(left = 0.08, bottom = 0.30, top = 0.92, right = 0.95)
	
	l_S, = plt.plot(tt, S, label='Susceptibles')
	l_I, = plt.plot(tt, I, label='Infectés')
	l_R, = plt.plot(tt, R, label='Rétablis')
	l_D, = plt.plot(tt, D, label='Morts')
	# plt.plot(tt, K_SI, label='K_SI')
	
	main_ax = plt.gca()
	main_ax.set_xlim([0, 400])
	main_ax.set_ylim([0, 100])
	plt.legend()
	plt.title('Modèle SIR(D) - Population [%]')
	
	axcolor = 'lightgoldenrodyellow'	
	ax_hi_t = plt.axes([0.30, 0.22, 0.55, 0.03], facecolor=axcolor)
	ax_K_SI = plt.axes([0.30, 0.16, 0.55, 0.03], facecolor=axcolor)
	ax_K_IR = plt.axes([0.30, 0.12, 0.55, 0.03], facecolor=axcolor)
	ax_K_ID = plt.axes([0.30, 0.08, 0.55, 0.03], facecolor=axcolor)
	ax_K_RS = plt.axes([0.30, 0.04, 0.55, 0.03], facecolor=axcolor)
	
	s_hi_t = Slider(ax_hi_t, 'Ajustement du temps'      , 1, t_size, valinit = 100  , valfmt='%d', valstep = 1)
	s_K_SI = Slider(ax_K_SI, 'Susceptibles -> Infectés' , 0, 1.00, valinit = 0.900, valfmt='%1.4f')
	s_K_IR = Slider(ax_K_IR, 'Infectés -> Rétablis'     , 0, 1.00, valinit = 0.500, valfmt='%1.4f')
	s_K_ID = Slider(ax_K_ID, 'Infectés -> Morts'        , 0, 0.01, valinit = 0.009, valfmt='%1.4f')
	s_K_RS = Slider(ax_K_RS, 'Rétablis -> Susceptibles' , 0, 0.01, valinit = 0.000, valfmt='%1.4f')
	
	update(0)
	
	s_hi_t.on_changed(update)
	s_K_ID.on_changed(update)
	s_K_SI.on_changed(update)
	s_K_IR.on_changed(update)
	s_K_RS.on_changed(update)
	
	resetax = plt.axes([0.01, 0.95, 0.3, 0.04])
	button = Button(resetax, 'Réinitialiser les curseurs', color=axcolor, hovercolor='0.8')

	def reset(event):
		s_hi_t.reset()
		s_K_ID.reset()
		s_K_SI.reset()
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

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
	
	t_size = 400
	tt = np.array(range(t_size))
	
	# population size
	N = 100
	
	#
	# K_ID = 0.001-0*tt/t_size
	# K_SI = 0.3+0*tt/t_size
	# K_IR = 0.1+0*tt/t_size
	# K_RS = 0.005-0*tt/t_size

	D = np.zeros_like(tt, dtype = np.float); D[0] = 0
	I = np.zeros_like(tt, dtype = np.float); I[0] = 0.1
	R = np.zeros_like(tt, dtype = np.float); R[0] = 0.1
	S = np.zeros_like(tt, dtype = np.float); S[0] = N - D[0] - I[0] - R[0]

	def update(val):
		K_ID = s_K_ID.val
		K_SI = s_K_SI.val
		K_IR = s_K_IR.val	
		K_RS = s_K_RS.val	
		
		for t in tt[:-1]:
			
			# initialise to previous value
			D[t+1] = D[t]
			R[t+1] = R[t]
			I[t+1] = I[t]
			
			# some people die, they are not ill anymore
			D[t+1] += K_ID*I[t]
			I[t+1] -= K_ID*I[t]
			
			# from those who didn't die some people recover, they are not ill anymore
			# also some people who recovered, become susceptibles again
			R[t+1] += K_IR*I[t+1] - K_RS*R[t]
			I[t+1] -= K_IR*I[t+1]
			
			# more people get ill,and it is more likely if the number of susceptibles is big
			I[t+1] += K_SI*I[t+1]*S[t]/N
			I[t+1] = min(N, I[t+1])
			
			# susceptibles are all people who are not dead, who have not recovered and or not ill
			S[t+1] = N - D[t+1] - R[t+1] - I[t+1]
		
		l_I.set_ydata(I)
		l_R.set_ydata(R)
		l_D.set_ydata(D)
		l_S.set_ydata(S)
		
		fig.canvas.draw_idle()
	
	fig, ax = plt.subplots(num="SIR Model")
	plt.subplots_adjust(left=0.10, bottom=0.30)
	
	l_S, = plt.plot(tt, S, label='Susceptible')
	l_I, = plt.plot(tt, I, label='Infected')
	l_R, = plt.plot(tt, R, label='Recovered')
	l_D, = plt.plot(tt, D, label='Dead')
	# plt.plot(tt, K_SI, label='K_SI')
	
	# ax.set_yscale('log')
	# plt.gca().set_ylim([0.1, 100])
	plt.gca().set_ylim([0, 100])
	plt.legend()
	plt.title('SIR Model - Population [%]')
	
	axcolor = 'lightgoldenrodyellow'	
	ax_K_SI = plt.axes([0.35, 0.20, 0.55, 0.04], facecolor=axcolor)
	ax_K_IR = plt.axes([0.35, 0.15, 0.55, 0.04], facecolor=axcolor)
	ax_K_ID = plt.axes([0.35, 0.10, 0.55, 0.04], facecolor=axcolor)
	ax_K_RS = plt.axes([0.35, 0.05, 0.55, 0.04], facecolor=axcolor)
	
	s_K_SI = Slider(ax_K_SI, 'Susceptible -> Infected' , 0, 1.00, valinit = 0.300, valfmt='%1.4f')
	s_K_IR = Slider(ax_K_IR, 'Infected -> Recovered'   , 0, 1.00, valinit = 0.100, valfmt='%1.4f')
	s_K_ID = Slider(ax_K_ID, 'Infected -> Dead'        , 0, 0.01, valinit = 0.001, valfmt='%1.4f')
	s_K_RS = Slider(ax_K_RS, 'Recovered -> Susceptible', 0, 0.01, valinit = 0.000, valfmt='%1.4f')
	
	update(0)
	
	s_K_ID.on_changed(update)
	s_K_SI.on_changed(update)
	s_K_IR.on_changed(update)
	s_K_RS.on_changed(update)
	
	resetax = plt.axes([0.1, 0.9, 0.1, 0.04])
	button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

	def reset(event):
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

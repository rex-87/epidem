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
	
	t_size = 400
	tt = np.array(range(t_size))
	
	# population size
	N = 100
	
	#
	K_D = 0.001-0*tt/t_size
	K_R = 0.1+0*tt/t_size
	K_I = 0.3+0*tt/t_size
	K_S = 0.005-0*tt/t_size
	
	D = np.zeros_like(tt, dtype = np.float); D[0] = 0
	I = np.zeros_like(tt, dtype = np.float); I[0] = 1
	R = np.zeros_like(tt, dtype = np.float); R[0] = 0
	S = np.zeros_like(tt, dtype = np.float); S[0] = N - D[0] - I[0] - R[0]
	
	for t in tt[:-1]:
		
		# initialise to previous value
		D[t+1] = D[t]
		R[t+1] = R[t]
		I[t+1] = I[t]
		
		# some people die, they are not ill anymore
		D[t+1] += K_D[t]*I[t]
		I[t+1] -= K_D[t]*I[t]
		
		# from those who didn't die some people recover, they are not ill anymore
		# also some people who recovered, become susceptibles again
		R[t+1] += K_R[t]*I[t+1] - K_S[t]*R[t]
		I[t+1] -= K_R[t]*I[t+1]
		
		# more people get ill,and it is more likely if the number of susceptibles is big
		I[t+1] += K_I[t]*I[t+1]*S[t]/N
		I[t+1] = min(N, I[t+1])
		
		# susceptibles are all people who are not dead, who have not recovered and or not ill
		S[t+1] = N - D[t+1] - R[t+1] - I[t+1]
	
	plt.plot(tt, I, label='I')
	plt.plot(tt, R, label='R')
	plt.plot(tt, D, label='D')
	plt.plot(tt, S, label='S')
	# plt.plot(tt, K_I, label='K_I')
	plt.legend()
	plt.show()

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	input("Press any key to exit ...")

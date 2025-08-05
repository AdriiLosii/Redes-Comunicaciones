import os #for fork
import signal #for signal
import sys
import time

def funcion_fillo(i):
	global variabel
	print("son o proceso ", os.getpid(), ", variabel= ", variabel, ", a durmir")
	time.sleep(7-i)
	variabel += i+1
	print("Son o proceso ", os.getpid(), ",espertando, variabel= ", variabel, ", a teminar")
	exit(0)
	
def signal_handler(signalNumber,frame):
	pid, status = os.waitpid(0,os.WNOHANG)
	if pid != 0:
		fillos.remove(pid)
		print("Proceso fillo ", pid, " saiu con estatus ", status)
	
	
if __name__ == "__main__":
	global variabel
	variabel = 10.5
	fillos = []
	signal.signal(signal.SIGCHLD,signal_handler)
	for i in range(3):
		newpid = os.fork()
		if newpid == 0:
			funcion_fillo(i)
		else:
			print("Son o proceso pai ", os.getpid(), " e creei un fillo ", newpid, ", variabel= ", variabel)
			fillos.append(newpid)
	print("Son o proceso pai ", os.getpid(), " a esperar que acaben os fillos")
	#pid, status = os.wait()
	#print("proceso fillo ", pid, " saiu con estatus ", status)
	while len(fillos) > 0:
		pass
	print("Son o proceso pai, acabaron todos os fillos, variabel= ", variabel)

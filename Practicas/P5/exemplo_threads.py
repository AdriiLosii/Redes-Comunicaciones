import os #for fork
import signal #for signal
import sys
import time
import threading



def funcion_fio(i):
	global variabel
	print("son o fio ",threading.current_thread().name, ", pid= ", os.getpid()," variabel= ", variabel, ", a durmir")
	time.sleep(7-i)
	variabel += i+1
	print("Son o fio ",threading.current_thread().name, ", pid= ", os.getpid(),", espertando, variabel= ", variabel, ", a teminar")
	exit(0)
	
	
if __name__ == "__main__":
	global variabel
	variabel = 10.5
	fios = []
	for i in range(3):
		x = threading.Thread(target=funcion_fio, args=(i,), name=i+1)
		print("Son o proceso pai ", os.getpid(), " e creei un fio ", x.name, ", variabel= ", variabel)
		fios.append(x)
		x.start()
	print("Son o proceso pai ", os.getpid(), " a esperar que acaben os fillos")
	for fio in fios:
		fio.join()
		print("Son o proceso pai, acabou o fillo ", fio.name," variabel= ", variabel)
	#while len(fios)>0:
	#	for fio in fios:
	#		if fio.is_alive()==0:
	#			print("Son o proceso pai, acabou o fillo ", fio.name," variabel= ", variabel)
	#			fios.remove(fio)
	print("Son o proceso pai, acabaron todos os fillos, variabel= ", variabel)

import socket
import argparse


def servidor(puerto):
	socket_server = socket.socket(family=socket.AddressFamily.AF_INET, type=socket.SocketKind.SOCK_STREAM, proto=socket.IPPROTO_TCP, fileno=None)    # Creamos el socket de tipo TCP

	try:
		address = ('', puerto)
		try:
			socket_server.bind(address)    # Le asignamos una direccion al socket creado
			socket_server.listen()  # Marcamos el socket como pasivo (socket servidor)
			i = 0

			while(True):
				socket_conn, address = socket_server.accept()    # Aceptamos la conexion y obtenemos el nuevo socket y la direccion
				print('Se ha conectado el cliente con IP: {}'.format(address[0]))

				while(True):
					# Recibimos la linea y mostramos el número de bytes recibidos por pantalla
					line = socket_conn.recv(1024)

					# Comprobamos que nos llegue información del cliente, en caso contrario, cerramos la conexión y salimso del bucle infinito.
					if (len(line) == 0):
						socket_conn.close()
						break

					print('Bytes recibidos:',len(line))

					# Pasamos los caracteres a mayúscula, devolvemos la linea y mostramos el número de bytes por pantalla
					lineCAP = line.decode().upper()
					bytes_sent = socket_conn.send(lineCAP.encode())
					print('Bytes enviados:',bytes_sent)


		except OSError as error:
			print(error)

	except Exception as error:
		print(error)
		print('Error desconocido al crear el servidor')


def main():
	try:
		# Creamos los argumentos para la introduccion de datos 
		parser = argparse.ArgumentParser(description='Práctica 2 de Redes y Comunicaciones')
		parser.add_argument('-p','--puerto',type=int,help='Un número de puerto')
		args=parser.parse_args()

		# "Switch" para ir a las funciones necesarias según los datos aportados
		if args.puerto:
			servidor(args.puerto)

	except Exception as error:	# Por si se introducen datos que no corresponden con los definidos en las funciones "parser.add_argument()"
		print(error)
		print('Datos introducidos no válidos')




if __name__ == "__main__":
    main()	
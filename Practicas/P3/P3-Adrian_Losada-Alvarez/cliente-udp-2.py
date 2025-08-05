# Importamos las librerías necesarias
import socket
import argparse
import binascii


# Función para comprobar que la ip es válida
def verificar_IP(ip):
	try:
		try:
			# Diferenciamos el tipo de ip entre IPv4 e IPv6
			if (socket.getaddrinfo(ip, None)[0][0] == socket.AddressFamily.AF_INET):	# Si la ip introducida es una IPv4, el tipo de dato sera 'socket.AddressFamily.AF_INET'
				binascii.hexlify(socket.inet_pton(socket.AF_INET, ip))	# Se deja esta linea para que salte un error de tipo 'socket.gaierror' si es una ip en binario/hexadecimal
				return ip

		# Si la ip introducida es una ip en binario/hexadecimal
		except socket.gaierror:
			try:
				packed_bin_ip = binascii.unhexlify(ip)	# Esta linea puede dar error si no es una IPv4
				return socket.inet_ntop(socket.AddressFamily.AF_INET, packed_bin_ip)	# Obtenemos la ip sin compactar y devolvemos datos

			except ValueError:	# Si no se trata de una IPv4 obtendremos un error de tipo ValueError ya que se trata de una IPv6
				return socket.inet_ntop(socket.AddressFamily.AF_INET6, packed_bin_ip)	# Obtenemos la ip sin compactar y devolvemos datos

	# Tratamiento de errores por si se introduce una ip no válida
	except UnboundLocalError as error:
		print(error)
		print('Error "UnboundLocalError": Dirección IP no válida (formato incorrecto)')

	except socket.herror as error:
		print(error)
		print('Error "socket.herror": Dirección IP no válida (no existe)')

	except Exception as error:
		print(error)

def envia(puerto_prop, ip, puerto_dest, archivo):
	# Diferenciamos entre una IPv4 o IPv6 al crear el socket
	if (socket.getaddrinfo(ip, puerto_dest)[0][0] == socket.AddressFamily.AF_INET):
		# Creamos el socket de tipo UDP
		socket_send = socket.socket(family=socket.AddressFamily.AF_INET, type=socket.SocketKind.SOCK_DGRAM, proto=socket.IPPROTO_UDP, fileno=None)
	else:
		# Creamos el socket de tipo UDP
		socket_send = socket.socket(family=socket.AddressFamily.AF_INET6, type=socket.SocketKind.SOCK_DGRAM, proto=socket.IPPROTO_UDP, fileno=None)

	try:
		# Definimos la dirección propia y se la asignamos al socket creado
		address_prop = ('', puerto_prop)
		socket_send.bind(address_prop)

		# Definimos la dirección destino
		address_dest = (ip, puerto_dest)

		with open(archivo+'.txt', 'r') as archive:
			with open(archivo+'CAP.txt', 'w') as archiveCAP:
				for line in archive:
					# Enviamos la linea y mostramos los bytes enviados por pantalla
					bytes_sent = socket_send.sendto(line.encode(), address_dest)
					print('Número de bytes enviados: {}'.format(bytes_sent))

					# Recepción de datos
					info = socket_send.recvfrom(1024)
					encoded_lineCAP = info[0]
					print('Número de bytes recibidos: {}\n'.format(len(encoded_lineCAP)))

					# Escribimos la línea recibida en el nuevo archivo
					archiveCAP.write(encoded_lineCAP.decode())

				# Mensaje para indicar el final del texto
				socket_send.sendto('FIN_DEL_MENSAJE'.encode(), address_dest)

		# Cerramos el socket
		socket_send.close()

	# Tratamiento de errores
	except ConnectionRefusedError as error:
		print(error)
		print('Error "ConnectionRefusedError": Conexión rechazada')

	except Exception as error:
		print(error)


def main():
	try:
		# Creamos los argumentos para la introducción de datos 
		parser = argparse.ArgumentParser(description='Práctica 2 de Redes y Comunicaciones')
		parser.add_argument('-pp','--puerto_prop',type=int,help='Un número de puerto propio')
		parser.add_argument('-i','--ip',type=str,help='Una ip, en IPv4, IPv6 o entero hexadecimal')
		parser.add_argument('-pd','--puerto_dest',type=int,help='Un número de puerto destinatario')
		parser.add_argument('-a','--archivo',type=str,help='Un archivo de texto (sin agregar ".txt")')
		args=parser.parse_args()

		# Si se introdujeron los argumentos necesarios el programa continúa
		if(args.puerto_prop and args.ip and args.puerto_dest and args.archivo):
			envia(args.puerto_prop, verificar_IP(args.ip), args.puerto_dest, args.archivo)
		else: raise TypeError

	# Tratamiento de errores
	except TypeError as error:
		print("Error: Argumentos introducidos insuficientes")

	except Exception as error:
		print(error)




if __name__ == "__main__":
    main()		
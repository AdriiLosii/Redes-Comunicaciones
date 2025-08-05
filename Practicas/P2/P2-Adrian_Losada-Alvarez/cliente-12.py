import socket
import argparse
import binascii


def verificar_IP(ip):
	try:
		try:
			# Diferenciamos el tipo de ip entre IPv4 e IPv6
			if (socket.getaddrinfo(ip, None)[0][0] == socket.AddressFamily.AF_INET):	# Si la ip introducida es una IPv4, el tipo de dato sera 'socket.AddressFamily.AF_INET'
				binascii.hexlify(socket.inet_pton(socket.AF_INET, ip))	# Se deja esta linea para que salte un error de tipo 'socket.gaierror' si es una ip en binario/hexadecimal
				return ip

		except socket.gaierror:	# Si la ip introducida es una ip en binario/hexadecimal nos daran errores las lineas 35 o 37
			try:
				packed_bin_ip = binascii.unhexlify(ip)	# Esta linea puede dar error si no es una IPv4
				return socket.inet_ntop(socket.AddressFamily.AF_INET, packed_bin_ip)	# Obtenemos la ip sin compactar y devolvemos datos

			except ValueError:	# Si no se trata de una IPv4 obtendremos un error de tipo ValueError ya que se trata de una IPv6
				return socket.inet_ntop(socket.AddressFamily.AF_INET6, packed_bin_ip)	# Obtenemos la ip sin compactar y devolvemos datos

	# Tratamiento de errores por si se introduce una ip no valida
	except UnboundLocalError as error:
		print(error)
		print('Error "UnboundLocalError": Dirección IP no válida (formato incorrecto)')

	except socket.herror as error:
		print(error)
		print('Error "socket.herror": Dirección IP no válida (no existe)')

	except Exception as error:
		print(error)
		print('Error desconocido')

def cliente(ip, puerto):
	# Diferenciamos entre una IPv4 o IPv6 al crear el socket
	if (socket.getaddrinfo(ip, puerto)[0][0] == socket.AddressFamily.AF_INET):
		socket_client = socket.socket(family=socket.AddressFamily.AF_INET, type=socket.SocketKind.SOCK_STREAM, proto=socket.IPPROTO_TCP, fileno=None)    # Creamos el socket de tipo TCP
	else:
		socket_client = socket.socket(family=socket.AddressFamily.AF_INET6, type=socket.SocketKind.SOCK_STREAM, proto=socket.IPPROTO_TCP, fileno=None)    # Creamos el socket de tipo TCP

	address = (ip, puerto)
	try:
		print('Conectando con el servidor...')
		socket_client.connect(address)	# Marcamos el socket como activo (socket cliente)
		print('Conexión al servidor establecida')
		msg = socket_client.recv(1024)	# Recepcion de datos
		print('Mensaje recibido:',msg.decode())
		print('Número de bytes:', len(msg))
		socket_client.close()

	except ConnectionRefusedError as error:
		print(error)
		print('Error "ConnectionRefusedError": Conexión rechazada')


def main():
	try:
		# Creamos los argumentos para la introduccion de datos 
		parser = argparse.ArgumentParser(description='Práctica 2 de Redes y Comunicaciones')
		parser.add_argument('-i','--ip',type=str,help='Una ip, en IPv4, IPv6 o entero hexadecimal')
		parser.add_argument('-p','--puerto',type=int,help='Un número de puerto')
		args=parser.parse_args()


		# "Switch" para ir a las funciones necesarias según los datos aportados
		if (args.ip and args.puerto):
			cliente(verificar_IP(args.ip), args.puerto)

		

	except Exception as error:	# Por si se introducen datos que no corresponden con los definidos en las funciones "parser.add_argument()"
		print(error)
		print('Datos introducidos no válidos')




if __name__ == "__main__":
    main()		
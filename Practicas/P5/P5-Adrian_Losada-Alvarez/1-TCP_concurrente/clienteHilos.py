import socket
import argparse
import binascii
import threading


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

def manejar_cliente(ip, puerto):
    if (socket.getaddrinfo(ip, puerto)[0][0] == socket.AF_INET):
        socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    else:
        socket_client = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

    address = (ip, puerto)
    try:
        print(f'Conectando con el servidor desde el hilo {threading.current_thread().name}...')
        socket_client.connect(address)
        print(f'Conexión al servidor establecida desde el hilo {threading.current_thread().name}')

        # Recepción de 2 mensajes
        for _ in range(2):
            msg = socket_client.recv(1024)
            print(f'Soy el hilo {threading.current_thread().name} y he recibido el mensaje: {msg.decode()}')

        socket_client.close()
        print(f'Soy el hilo {threading.current_thread().name} y he cerrado mi conexión.')

    except ConnectionRefusedError as error:
        print(error)
        print('Error "ConnectionRefusedError": Conexión rechazada')

def cliente(ip, puerto, num_clientes):
    for i in range(num_clientes):
        # Crear un hilo para manejar el cliente
        thread = threading.Thread(target=manejar_cliente, args=(ip, puerto))
        thread.start()

def main():
    try:
        parser = argparse.ArgumentParser(description='Práctica 5 de Redes y Comunicaciones')
        parser.add_argument('-i', '--ip', type=str, help='Una ip, en IPv4, IPv6 o entero hexadecimal')
        parser.add_argument('-p', '--puerto', type=int, help='Un número de puerto')
        parser.add_argument('-n', '--num_clientes', type=int, help='Número de clientes')
        args = parser.parse_args()

        if args.ip and args.puerto and args.num_clientes:
            cliente(verificar_IP(args.ip), args.puerto, args.num_clientes)
        else:
            print('Faltan argumentos. Utiliza "-i", "-p" y "-n" para especificar la IP, puerto y número de clientes respectivamente.')

    except Exception as error:
        print(error)
        print('Datos introducidos no válidos')

if __name__ == "__main__":
    main()
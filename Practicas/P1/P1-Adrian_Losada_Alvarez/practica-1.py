import socket
import binascii
import argparse


def nombre_host(nombre):
	try:
		# Obtenemos la lista con toda la información del nombre de host introducido y seleccionamos los datos que nos interesan para mostrarlos
		info = socket.getaddrinfo(nombre, None)
		print('Nombre canónico:',nombre)
		for i in range(len(info)):
			if (info[i][0] == socket.AddressFamily.AF_INET):
				print('Dirección IPv4: {}; binario: {}; puerto: {}'.format(info[i][4][0], binascii.hexlify(socket.inet_pton(socket.AF_INET, info[i][4][0])),  info[i][2]))
			else:
				try:
					print('Dirección IPv6: {}; binario: {}; puerto: {}'.format(info[(i)][4][0], binascii.hexlify(socket.inet_pton(socket.AF_INET6, info[(i)][4][0])),  info[i][2]))
				except OSError: # Tratamiento de errores por si el nombre de host introducido no tiene dirección IPv6
					print('Dirección IPV6: Esta dirección non ten IPv6')

	except socket.gaierror as err:	# Tratamiento de errores por si se introduce una IP que no existe
		print(err)
		print('Error "socket.gaierror": Nombre de host no válido (no existe)')

	except:
		print('Error desconocido')

def servicio(str_servicio):
	try:
		# Obtenemos las listas con la informacion del servicio dado y seleccionamos el dato que nos interesa
		list_service = socket.getaddrinfo(None, str_servicio)
		print('Servicio {}: puerto {}'.format(str_servicio, list_service[len(list_service)-1][4][1]))

	except socket.gaierror as err:	# Tratamiento de errores por si se introduce un nombre de servicio que no existe
		print(err)
		print('Error "socket.gaierror": Nombre de servicio no válido (no existe)')

	except:
		print('Error desconocido')

def ip(ip):
	try:
		try:
			# Diferenciamos el tipo de ip entre IPv4 e IPv6
			if (socket.getaddrinfo(ip, None)[0][0] == socket.AddressFamily.AF_INET):	# Si la ip introducida es una IPv4, el tipo de dato sera 'socket.AddressFamily.AF_INET'
				print('Dirección IPv4 {} : {} : host {}'.format(ip, binascii.hexlify(socket.inet_pton(socket.AF_INET, ip)), socket.getnameinfo((ip, 80), socket.NI_NOFQDN)[0]))		# Esta linea puede dar error si es una ip en binario/hexadecimal
			else:	# Si el tipo de dato no es 'socket.AddressFamily.AF_INET' (IPv4) se trata de una ip de tipo 'socket.AddressFamily.AF_INET6' (IPv6)
				print('Dirección IPv6 {} : {} : host {}'.format(ip, binascii.hexlify(socket.inet_pton(socket.AF_INET6, ip)), socket.getnameinfo((ip, 80), socket.NI_NOFQDN)[0]))	# Esta linea puede dar error si es una ip en binario/hexadecimal

		except socket.gaierror:	# Si la ip introducida es una ip en binario/hexadecimal nos daran errores las lineas 35 o 37
			try:
				packed_bin_ip = binascii.unhexlify(ip)	# Esta linea puede dar error si no es una IPv4
				unpacked_ip = socket.inet_ntop(socket.AddressFamily.AF_INET, packed_bin_ip)		# Obtenemos la ip sin compactar y mostramos los datos solicitados
				print('Dirección IPv4 {} : {} : host {}'.format(unpacked_ip, ip, socket.getnameinfo((unpacked_ip, 80), socket.NI_NOFQDN)[0]))

			except ValueError:	# Si no se trata de una IPv4 obtendremos un error de tipo ValueError ya que se trata de una IPv6
				unpacked_ip = socket.inet_ntop(socket.AddressFamily.AF_INET6, packed_bin_ip)	# Obtenemos la ip sin compactar y mostramos los datos solicitados
				print('Dirección IPv6 {} : {} : host {}'.format(unpacked_ip, ip, socket.getnameinfo((unpacked_ip, 80), socket.NI_NOFQDN)[0]))

	# Tratamiento de errores por si se introduce una ip no valida
	except UnboundLocalError as err:
		print(err)
		print('Error "UnboundLocalError": Dirección IP no válida (formato incorrecto)')

	except socket.herror as err:
		print(err)
		print('Error "socket.herror": Dirección IP no válida (no existe)')

	except:
		print('Error desconocido')

def puerto(puerto):
	try:
		# Mostramos el puerto y su servicio correspondiente con las funcion socket.getservbyport()
		print('Puerto {}: servicio {}'.format(puerto, socket.getservbyport(puerto)))

	except OSError as err:	# Tratamiento de errores por si se introduce un puerto que no existe
		print(err)
		print('Error "OSError": Número de puerto no válido (no existe)')

	except:
		print('Error desconocido')


def main():
	try:
		# Creamos los argumentos para la introduccion de datos 
		parser = argparse.ArgumentParser(description='Práctica 1 de Redes e Comunicacións')
		parser.add_argument('-n','--nome_host',type=str,help='Un nome de dirección de internet, coma www.usc.es')
		parser.add_argument('-s','--servizo',type=str,help='Un nome de sevizo, coma ssh')
		parser.add_argument('-i','--ip',type=str,help='Unha ip, en IPv4, IPv6 ou enteiro hexadecimal')
		parser.add_argument('-p','--porto',type=int,help='Un numero de porto, coma 22')
		args=parser.parse_args()

		# "Switch" para ir a las funciones necesarias según los datos aportados
		if (args.nome_host or args.servizo or args.ip or args.porto):
			print('****************************************************************')

		if args.nome_host:
			nombre_host(args.nome_host)
			print('****************************************************************')

		if args.servizo:
			servicio(args.servizo)
			print('****************************************************************')

		if args.ip:
			ip(args.ip)
			print('****************************************************************')

		if args.porto:
			puerto(args.porto)
			print('****************************************************************')

	except:	# Por si se introducen datos que no corresponden con los definidos en las funciones "parser.add_argument()"
		print('****************************************************************')
		print('Datos introducidos no válidos')
		print('****************************************************************')




if __name__ == "__main__":
    main()		
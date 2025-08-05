# Importamos las librerías necesarias
import socket
import argparse


def recibe(puerto_prop):
    # Creamos el socket de tipo UDP
    socket_recv = socket.socket(family=socket.AddressFamily.AF_INET, type=socket.SocketKind.SOCK_DGRAM, proto=socket.IPPROTO_UDP, fileno=None)

    try:
        # Le asignamos una direccion vacía y un puerto propio al socket creado
        address_prop = ('', puerto_prop)
        socket_recv.bind(address_prop)

        while(True):
            # Recibimos la linea y mostramos el número de bytes recibidos por pantalla
            info = socket_recv.recvfrom(1024)
            encoded_line = info[0]
            address_dest = (info[1][0], info[1][1])

            if(encoded_line.decode() == 'FIN_DEL_MENSAJE'):
                socket_recv.close()
                break

            print('Bytes recibidos de socket con IP: {}; y puerto: {}'.format(address_dest[0], address_dest[1]))
            print('Número de bytes recibidos: {}'.format(len(encoded_line)))

            # Pasamos los caracteres a mayúscula, devolvemos la línea y mostramos el número de bytes enviados
            decoded_lineCAP = encoded_line.decode().upper()
            bytes_sent = socket_recv.sendto(decoded_lineCAP.encode(), address_dest)
            print('Bytes enviados a socket con IP: {}; y puerto: {}'.format(address_dest[0], address_dest[1]))
            print('Número de bytes enviados: {}\n'.format(bytes_sent))

        # Cerramos el socket
        socket_recv.close()

    # Tratamiento de errores
    except OSError as error:
        print(error)
        print('Error "OSError": Dirección en uso')

    except Exception as error:
        print(error)


def main():
    try:
        # Creamos los argumentos para la introducción de datos 
        parser = argparse.ArgumentParser(description='Práctica 2 de Redes y Comunicaciones')
        parser.add_argument('-pp','--puerto_prop',type=int,help='Un número de puerto propio')
        args=parser.parse_args()

        # Si se introdujeron los argumentos necesarios el programa continúa
        if(args.puerto_prop):
            recibe(args.puerto_prop)
        else: raise TypeError

    # Tratamiento de errores
    except TypeError as error:
        print("Error: Argumentos introducidos insuficientes")

    except Exception as error:
        print(error)




if __name__ == "__main__":
    main()	
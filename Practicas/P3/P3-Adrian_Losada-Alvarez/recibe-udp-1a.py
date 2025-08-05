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

        # Recibimos el mensaje e imprimimos toda la información obtenida
        info = socket_recv.recvfrom(1024)
        print('Se ha conectado el cliente con IP: {}; y puerto: {}'.format(info[1][0], info[1][1]))
        print('Mensaje recibido: {}'.format(info[0].decode()))

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
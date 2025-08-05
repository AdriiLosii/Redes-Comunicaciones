import socket
import argparse
import os
import time


def manejar_cliente(socket_conn, address):
    print(f'Soy el proceso hijo {os.getpid()} y se ha conectado el cliente con IP: {address[0]}')

    # Se envia el primer mensaje
    msg1 = 'Hello world!'
    socket_conn.send(msg1.encode())

    # Dormir durante 5 segundos
    time.sleep(5)

    # Se envia el segundo mensaje
    msg2 = 'Msg after sleeping'
    socket_conn.send(msg2.encode())

    # Cerramos la conexión
    socket_conn.close()
    print(f'Soy el proceso hijo {os.getpid()} y he cerrado mi conexión.')

def servidor(puerto):
    socket_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

    try:
        address = ('', puerto)
        socket_server.bind(address)
        socket_server.listen()
        print(f'Servidor creado por el proceso padre {os.getpid()}')

        while(True):
            socket_conn, address = socket_server.accept()

            # Creamos un proceso hijo
            pid = os.fork()

            if pid == 0:
                # Código ejecutado por los procesos hijos
                manejar_cliente(socket_conn, address)
                break
            else:
                # Código ejecutado por el proceso padre
                socket_conn.close()

    except OSError as error:
        print(error)
        print('Error "OSError": Dirección en uso')

    except Exception as error:
        print(error)
        print('Error desconocido al crear el servidor')

def main():
    try:
        parser = argparse.ArgumentParser(description='Práctica 5 de Redes y Comunicaciones')
        parser.add_argument('-p', '--puerto', type=int, help='Un número de puerto')
        args = parser.parse_args()

        if args.puerto:
            servidor(args.puerto)
        else:
            print('Faltan argumentos. Utiliza "-p" para especificar el puerto.')

    except Exception as error:
        print(error)
        print('Datos introducidos no válidos')

if __name__ == "__main__":
    main()
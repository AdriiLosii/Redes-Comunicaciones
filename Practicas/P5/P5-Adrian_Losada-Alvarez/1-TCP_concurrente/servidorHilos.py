import socket
import argparse
import threading
import time


def manejar_cliente(socket_conn, address):
    print(f'Soy el hilo {threading.current_thread().name} y se ha conectado el cliente con IP: {address[0]}')

    # Se envía el primer mensaje
    msg1 = 'Hello world!'
    socket_conn.send(msg1.encode())

    # Dormir durante 5 segundos
    time.sleep(5)

    # Se envía el segundo mensaje
    msg2 = 'Msg after sleeping'
    socket_conn.send(msg2.encode())

    # Cerramos la conexión
    socket_conn.close()
    print(f'Soy el hilo {threading.current_thread().name} y he cerrado mi conexión.')

def servidor(puerto):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        address = ('', puerto)
        socket_server.bind(address)
        socket_server.listen()
        print(f'Servidor creado por el hilo principal {threading.current_thread().name}')

        while True:
            socket_conn, address = socket_server.accept()

            # Creamos un hilo para manejar el cliente
            thread = threading.Thread(target=manejar_cliente, args=(socket_conn, address))
            thread.start()

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
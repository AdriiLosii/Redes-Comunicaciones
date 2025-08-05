import socket
import argparse
import os
import threading


def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f'Recibido: {request_data}')

    # Obtener la ruta del recurso solicitado
    resource_path = request_data.split()[1]

    # Verificar si el recurso existe
    if os.path.isfile("./recursos/" + resource_path):
        # Leer el contenido del archivo
        with open("./recursos/" + resource_path, 'r') as file:
            content = file.read()

        response = f"HTTP/1.0 200 OK\nContent-Type: text/html\n\n{content}"
    else:
        # Recurso no encontrado
        response = "HTTP/1.0 404 Not Found\nContent-Type: text/html\n\nPagina no encontrada"

    # Enviar la respuesta al cliente
    client_socket.send(response.encode('utf-8'))

    # Cerrar la conexión
    client_socket.close()

def start(server, puerto, concurrencia):
    print(f'Servidor HTTP iniciado en el puerto {puerto} con {concurrencia} concurrentes')

    if(concurrencia == 'thread'):
        while(True):
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_request, args=(client_socket,))
            thread.start()

    elif(concurrencia == 'process'):
        while(True):
            client_socket, addr = server.accept()
            pid = os.fork()
            if pid == 0:
                # Proceso hijo
                handle_request(client_socket)
                os._exit(0)
            else:
                # Proceso padre
                client_socket.close()

    else:
        raise ValueError('El tipo de concurrencia debe ser "thread" o "process"')

def serverHTTP(puerto, concurrencia):
    """
    Mejoras implementadas en el servidor HTTP:
    - Concurrente (opción entre procesos o hilos)
    - Capaz de cargar las páginas de ejemplo
    - Muestra el mensaje un mensaje "Pagina no encontrada" si se busca algo que no existe
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', puerto))
    server_socket.listen(5)

    start(server_socket, puerto, concurrencia)

def main():
    try:
        parser = argparse.ArgumentParser(description='Práctica 5 de Redes y Comunicaciones')
        parser.add_argument('-p', '--puerto', type=int, help='Un número de puerto')
        parser.add_argument('-c', '--concurrencia', choices=['thread', 'process'], default='thread', help='El tipo de concurrencia (thread o process)')
        args = parser.parse_args()

        if args.puerto:
            serverHTTP(args.puerto, args.concurrencia)
        else:
            print(
                'Faltan argumentos. Utiliza "-p" y "-c" para especificar el puerto y el tipo de concurrencia ("thread" (por defecto) o "process").')

    except Exception as error:
        print(error)
        print('Error al iniciar el servidor HTTP')

if __name__ == "__main__":
    main()
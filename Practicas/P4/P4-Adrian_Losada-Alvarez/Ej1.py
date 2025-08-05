import argparse
import ipaddress

# Función para cargar la tabla de reenvío desde un archivo
def cargar_tabla(archivo):
    tabla = {}
    with open(archivo, 'r') as file:
        for linea in file:
            direccion, interfaz = linea.strip().split(',')
            tabla[direccion] = int(interfaz)
    return tabla

# Función para imprimir la información de la tabla de reenvío
def tabla(tabla_reenvio):
    try:
        tabla = cargar_tabla(tabla_reenvio)

        for direccion, interfaz in tabla.items():
            red = ipaddress.ip_network(direccion, strict=False)
            print(f"Dirección de red: {red.network_address}")
            print(f"Máscara de red: {red.netmask}")
            print(f"Longitud del prefijo: {red.prefixlen}")
            print(f"Número de direcciones: {red.num_addresses}")
            print(f"Rango de direcciones: {red.network_address} - {red.broadcast_address}")
            print(f"Interfaz: {interfaz}")
            print()

    except Exception as error:
        print(error)

# Función para verificar si una dirección IP pertenece a una red utilizando el operador 'in'
def pertenece_red_in(direccion, red):
    print('¿Dirección: {} pertenece a la red: {}? -> {}'.format(direccion, red, ipaddress.ip_address(direccion) in ipaddress.ip_network(red)))
    return ipaddress.ip_address(direccion) in ipaddress.ip_network(red)

# Función para verificar si una dirección IP pertenece a una red utilizando operaciones matemáticas con enteros
def pertenece_red_op_matematicas(direccion, red):
    try:
        direccion_lista = list(map(int, direccion.split('.')))
        direccion_entero = (direccion_lista[0] << 24) + (direccion_lista[1] << 16) + (direccion_lista[2] << 8) + direccion_lista[3]

        red_lista = list(map(int, red.split('/')[0].split('.')))
        red_entero = (red_lista[0] << 24) + (red_lista[1] << 16) + (red_lista[2] << 8) + red_lista[3]

        mascara = int(red.split('/')[1])
        mascara_binaria = (1 << 32) - (1 << (32 - mascara))

        return direccion_entero & mascara_binaria == red_entero & mascara_binaria

    except Exception as error:
        print(error)
        return False  # En caso de direcciones inválidas

# Función para encontrar la interfaz de salida basada en la dirección IP utilizando el operador 'in' y operaciones matemáticas
def encontrar_interfaz(tabla_reenvio, ip):
    max_prefijo_in = 0
    interfaz_salida_in = 0
    max_prefijo_op_mat = 0
    interfaz_salida_op_mat = 0
    tabla = cargar_tabla(tabla_reenvio)

    for direccion, interfaz in tabla.items():
        red, mascara = direccion.split('/')
        # Con "in"
        if pertenece_red_in(ip, direccion) and int(mascara) > max_prefijo_in:
            max_prefijo_in = int(mascara)
            interfaz_salida_in = interfaz

        # Con operaciones matemáticas
        if pertenece_red_op_matematicas(ip, direccion) and int(mascara) > max_prefijo_op_mat:
            max_prefijo_op_mat = int(mascara)
            interfaz_salida_op_mat = interfaz
    
    return max_prefijo_in, interfaz_salida_in, max_prefijo_op_mat, interfaz_salida_op_mat

# Función principal del programa
def tabla_ip(tabla_reenvio, ip):
    try:
        # Llamamos a las dos funciones creadas para comprobar la pertenencia a cada red
		# Conclusión: A función implementada con operaciones matemáticas debe de ser más rápida,
		# ya que las operaciones con enteros suelen ser más eficientes a nivel de procesamiento en comparación
		# con la manipulación de objetos de 'ip_address' e 'ip_network' que involucran conversiones y comparaciones
		# más complejas.
        interfaz_salida_in, bits_prefijo_in, interfaz_salida_op_mat, bits_prefijo_op_mat = encontrar_interfaz(tabla_reenvio, ip)
        print("\nCon comprobación de pertenencia al conjunto (con 'in')")
        print(f"Interfaz de salida escogido: {interfaz_salida_in}")
        print(f"Número de bits del prefijo: {bits_prefijo_in}")

        print("\nCon operaciones matematicas con enteros")
        print(f"Interfaz de salida escogido: {interfaz_salida_op_mat}")
        print(f"Número de bits del prefijo: {bits_prefijo_op_mat}")

    except Exception as error:
        print(error)

# Función principal para manejar los argumentos de entrada
def main():
    try:
        # Creamos los argumentos para la introducción de datos 
        parser = argparse.ArgumentParser(description='Práctica 2 de Redes y Comunicaciones')
        parser.add_argument('-tr','--tabla_reenvio',type=str,help='Un archivo con una tabla de reenvío (sin agregar ".txt")')
        parser.add_argument('-i','--ip',type=str,help='Una ip, en IPv4, IPv6 o entero hexadecimal')
        args = parser.parse_args()

        # Si se introdujeron los argumentos necesarios el programa continúa
        if args.tabla_reenvio and args.ip is None:	# Si solo se introduce la tabla de reenvío
            tabla(args.tabla_reenvio)
        elif args.tabla_reenvio and args.ip:		# Si se introduce la tabla de reenvío y una IP
            tabla_ip(args.tabla_reenvio, args.ip)
        else:
            raise TypeError

    # Tratamiento de errores
    except TypeError as error:
        print("Error: Argumentos introducidos insuficientes")

    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
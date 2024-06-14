# libreria generica
from socket import *
from datetime import datetime
import os
import json
import hashlib

# Funcion para enviar comandos a un server
def enviar_comando(host, port, comando):
    s = socket(AF_INET, SOCK_STREAM)    # Crear socket
    s.connect((host, port))             # Conectar con el servidor
    s.send(comando.encode())            # Enviamos el mensaje codificado
    data = s.recv(1024).decode()        # Decodificamos el mensaje recibido del server
    #print("Mensaje recibido:", data)
    s.close()                           # Cerramos la conexion con el servidor
    return data
#fin_enviar_comando

def archivo_existe(filename):
    return os.path.exists(filename)

def directorio_existe(dirname):
    return os.path.exists(dirname)

#todo: leer archivo
def leer_archivo(nombre):
    datos=[]
    with open(nombre, 'r') as archivo:
         for linea in archivo:
            datos.append(json.loads(linea))
    return datos
#fin_leer_archivo

#todo: guardar_archivo
def guardar_archivo(data, nombre):
     with open(nombre, "w", encoding="utf-8") as file:
          for item in data:
               file.write(json.dumps(item) + '\n')
#fin_guardar_archivo

#todo: encriptar clave
def encript(data):
     return hashlib.sha256(data.encode()).hexdigest()
#fin_encript

#todo: buscar_igual
def buscar_igual(lista, key, val):
    for item in lista:
        data = item[key]
        if data == val:
            return True
    return False
#fin_buscar_igual

#todo: listar transacciones
def guardar_transaccion():
     pass
     



def limpiar_log_buffer(llb):
	del llb[:]
	return llb
#fin_limpiar_log_buffer

def guardar_log_buffer(buffer, filename):
	data = ""
	for item in buffer:
		data = data + item + "\n"
	#fin_for
	guardar_archivo(filename, data)

def agregar_log_buffer(buffer, dato, max):
	# Si hay espacio en el logical log buffer
	if len(buffer)+1 <= max:
		buffer.append(dato)
	#fin_if
	return buffer	
#fin_guardar_log_buffer

def buffer_esta_lleno(buffer,max):
	return len(buffer) == max
#fin_buffer_esta_lleno

def registrar_info(llb, max, info, filename):
	# 0. Si el logical log buffer esta lleno
	#    a) lo guardamos en disco
	#    b) limpiamos el logical log buffer
	if buffer_esta_lleno(llb,max):
		guardar_log_buffer(llb, filename)
		llb = limpiar_log_buffer(llb)

	# 1. Guardamos los datos
	llb.append(info)

	# 2. Retornamos el logical log buffer
	return llb

#fin_registrar_data

def registrar_info_hdr(hdrb, hdrb_max, info, host, port):

    #0. Si el HDR Buffer esta lleno
    #       a) Enviamos la data al servidor HDR
    #       b) Limpiar el buffer HDR
    if buffer_esta_lleno(hdrb, hdrb_max):
        print("Enviando HDR Buffer al server HDR...")
        # Enviar data al server HDR
        for item in hdrb:
            comando = "REP " + item
            rpta = enviar_comando(host, port, comando)
            print("Rpta HDR:" + rpta)
        #fin_for
        hdrb = limpiar_log_buffer(hdrb)
    
    
    #1. SI no esta lleno, se guardan los datos en hdrb
    hdrb.append(info)
    
    #2. Retornamos el HDR buffer
    return hdrb

#fin_registrar_info_hdr

def leer_archivo_no_crlf(nombre):
	archivo = open(nombre)
	data = archivo.readlines()
	archivo.close()
	data_no_crlf = []
	for item in data:
		data_no_crlf.append(item.replace("\n",""))
	return data_no_crlf
#fin_leer_archivo

def get_fecha_y_hora():
    hora = datetime.now()
    return hora.strftime("%Y/%m/%d")
#def_get_fecha_y_hora

def cargar_dns_info(filename):
    dns_maps = {}
    if (archivo_existe(filename)):
        data = leer_archivo(filename)
        for linea in data:
            host = linea.split(":")[0]
            ip = linea.split(":")[1].replace("\n", "")
            dns_maps.setdefault(host, ip)
        #fin_for
    #fin_if
    return dns_maps
#fin_cargar_dns_info

def resolver_dns(host, dns_maps):
    if host in dns_maps:
        return dns_maps[host]
    else:
        return "IP_DESCONOCIDO"
#fin_resolver_dns

def guardar_email(buzon,user, subject, msg):
    # Guardar correo en formato simple
    mail = user + ":" + subject + ":" + msg + "\n"
    guardar_archivo(buzon, mail)
#fin_guarda_email

def obtener_email(buzon):
    # Si el buzon existe, leer correos del archivo
    if ( archivo_existe(buzon) ):
        data = leer_archivo(buzon)
        emails = ""
        for linea in data:
            emails += linea
        return emails
    else:
        return "Buzon vacio"
#fin_obtener_email


def buscar_mayorque(lista, key, val):
    res = []
    for item in lista:
        data = item[key]
        if data > val:
            res.append(item)
    #fin_for
    return res
#fin_buscar_mayorque

def buscar_menorque(lista, key, val):
    res = []
    for item in lista:
        data = item[key]
        if data < val:
            res.append(item)
    #fin_for
    return res
#fin_buscar_mayorque
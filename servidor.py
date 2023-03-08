import socket 
import os
from datetime import datetime
import time
import glob
import datetime
from ftplib import *
import sys
os.chdir("C:/xampp/htdocs/OneDrive/Documentos/my_app_wii")
def open_PD(port):
    print(port)
    global socket_control
    ip_servidor = '192.168.1.184'
    puerto_servidor = int(port)
    socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_control.bind(('', 20))
    socket_control.connect((ip_servidor, puerto_servidor))
    print(socket_control.recv(1024))
    print("Conectado")

def list_ftp():
    files = os.listdir('/') # Obtener la lista de archivos y directorios
    for file in files: # Iterar sobre la lista
        full_path = os.path.join('/',file) # Obtener la ruta completa del archivo o directorio
        if os.path.isfile(full_path): # Comprobar si es un archivo
            type = "type=file" # Asignar el tipo correspondiente
            size = "size=" + str(os.path.getsize(full_path)) # Obtener y formatear el tamaño en bytes
        elif os.path.isdir(full_path): # Comprobar si es un directorio
            type = "type=dir" # Asignar el tipo correspondiente
            size = "" # No asignar ningún tamaño
        
        modify = "modify=" + datetime.datetime.utcfromtimestamp(os.path.getmtime(full_path)).strftime("%Y%m%dT%H%M%SZ") # Obtener y formatear la fecha de modificación en UTC
        
        perm = "perm=rw" # Asignar unos permisos genéricos de lectura y escritura
        
        response = ";".join([type,size,modify,perm,file]) # Concatenar los pares de tipo-facto y el nombre del archivo o directorio
        
        socket_control.send(response.encode("utf-8")) # Enviar la respuesta al cliente
        socket_control.send("\n".encode("utf-8")) # Enviar un salto de línea para separar las respuestas
        socket_control.send("\r".encode("utf-8"))

def list_dir(conn):
    
        listdir = os.listdir("/")
        if not len(listdir):
            max_length = 0
        else:
            max_length = len(max(listdir, key=len))
        header = '| %*s | %9s | %12s | %20s | %11s | %12s |' % (max_length, 'Name', 'Filetype', 'Filesize', 'Last Modified', 'Permission', 'User/Group')
        table = '%s\n%s\n%s\n' % ('-' * len(header), header, '-' * len(header))
        conn.send(table.encode("utf-8"))
        
        for i in listdir:
            path = os.path.join(str(os.getcwd() + '///'), i)
            stat = os.stat(path)
            data = '| %*s | %9s | %12s | %20s | %11s | %12s |\n' % (max_length, i, 'Directory' if os.path.isdir(path) else 'File', str(stat.st_size) + 'B', time.strftime('%b %d, %Y %H:%M', time.localtime(stat.st_mtime))
                , oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid)) 
            conn.send(data.encode("utf-8"))
        
        table = '%s\n' % ('-' * len(header))
        conn.send(table.encode("utf-8"))
        conn.sendall(b'226 Directory send OK.\r\n')



def open_FTP():
    pc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    pc.bind(("192.168.1.184",21))
    pc.listen(5)
    conn, addr = pc.accept()
    print(f"Conexión establecida con {addr[0]}:{addr[1]}")
    conn.sendall(b'220 Bienvenido al servidor FTP\r\n')

    while conn:
        data = conn.recv(1024)
        if 'USER' in data.decode():
            print("User: "+data.decode())
            conn.sendall(b'230 User logged in, proceed\r\n')
        elif 'PASS' in data.decode():
            print("Password: "+data.decode())
            conn.sendall(b'230 User logged in, proceed\r\n')
            
        elif 'SYST' in data.decode():
            print("SYST")
            conn.sendall(b"215 Windows_NT\r\n")
            #conn.sendall(b"215 UNIX UNIX Type: L8\r\n")
        elif 'FEAT' in data.decode():
            conn.sendall(b"200 Command okay\r\n")
            print("FEAT")
            # Conexión socket establecida y recibido el comando FEAT
            
            conn.send(b"211-Features supported: EPRT\r\n")

        elif 'PWD' in data.decode():
            print("PWD")
            conn.sendall(str("257 "+os.getcwd()+ "/ is the current directory\r\n").encode())
        elif 'TYPE I' in data.decode():
            print("TYPE I")
            conn.sendall(b'200 Type set to I\r\n')
        elif 'TYPE A' in data.decode():
            print("TYPE A")
            conn.sendall(b'200 Type set to A\r\n')

        elif 'PASV' in data.decode():
            print("Entrando en metodo pasivo")
            
            conn.sendall(b"227 Entering Passive Mode (192,168,1,184,0,20))\r\n")
                
        elif 'PORT' in data.decode():
            print("PORT")
            port_ip = data.decode().split(',')
            print(port_ip)
            port = (int(port_ip[4]) * 256) + int(port_ip[5].replace('\r\n',''))
            conn.sendall(b"200 Command okay\r\n")

            #open_PD(port)
        elif 'CWD' in data.decode():
            print("CWD")
            os.chdir(data.decode().replace('CWD ','').replace('\r\n',''))
            conn.sendall(b"200 Command okay\r\n")
        elif 'LIST' in data.decode():
            conn.sendall(b"200 Command okay\r\n")
            file_list = os.listdir(".")    
            response = ""
            for file_name in file_list:
                file_stat = os.stat(file_name)
                file_size = file_stat.st_size
                file_time = file_stat.st_mtime
                file_perm = oct(file_stat.st_mode)[-4:]
                response += "type=file;size={};modify={};perm={}; {}\r\n".format(file_size, file_time, file_perm, file_name)
            # Enviar la respuesta al cliente FTP
            #conn.send(b"125 Data connection already open; transfer starting.\r\n") 
            conn.send(f"{response}\r\n".encode()) 
            conn.send(b"226 Directory send OK\r\n")

            

        elif data.decode() == "":
            break    
        print(f"Comando recibido: {data.decode()}")
        
    conn.close()
while True:
    try:

        
        open_FTP()
    except KeyboardInterrupt:
        # quit
        sys.exit()


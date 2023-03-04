import socket 
import os
from datetime import datetime
import time
import glob
from ftplib import *
def open_PD(port):
    print(port)
    ip_servidor = '192.168.1.184'
    puerto_servidor = int(port)
    socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_control.bind(('', 20))
    socket_control.connect((ip_servidor, puerto_servidor))

    while True:
        print(socket_control.recv(1024))
        break
    socket_control.close()







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
        elif 'FEAT' in data.decode():
            print("FEAT")
            conn.sendall(b'211 No features\r\n')
        elif 'PWD' in data.decode():
            print("PWD")
            conn.sendall(str("257 "+os.getcwd()+ " is the current directory\r\n").encode())
        elif 'TYPE I' in data.decode():
            print("TYPE I")
            conn.sendall(b'200 Type set to I\r\n')
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
        elif 'LIST' in data.decode():
            conn.sendall(b"200 Command okay\r\n")
            conn.sendall(b'125 Data connection already open; transfer starting.\r\n')
            
            files = os.listdir() # Obtener la lista de archivos y directorios
            for file in files: # Iterar sobre la lista
                conn.send(file.encode("utf-8")) # Enviar cada nombre al cliente
                conn.send("\n".encode("utf-8")) # Enviar un salto de línea para separar los nombres
            conn.send(b"\n\r")

            
            conn.sendall(b'250 Requested file action okay, completed.\r\n')
        elif data.decode() == "":
            break    
        print(f"Comando recibido: {data.decode()}")
        
    conn.close()
    

open_FTP()

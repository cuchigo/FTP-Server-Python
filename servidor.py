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
            conn.send(b"125 Data connection already open; transfer starting.\r\n") 
            conn.send(f"{response}\r\n".encode()) 
            conn.send(b"226 Directory send OK\r\n")

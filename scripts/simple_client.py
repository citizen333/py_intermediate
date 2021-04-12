import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.create_connection((HOST, PORT), 10) as s:
    outcoming_msg = 'a'*2000
    s.sendall(outcoming_msg.encode('utf8'))
    s.send(b'\0')
    incoming_msg = ''
    while True:
        data = s.recv(1024)
        if data[-1] == 0:
            incoming_msg += data.decode('utf8')[:-1]
            break
        incoming_msg += data.decode('utf8')
        
    print('Received', incoming_msg)
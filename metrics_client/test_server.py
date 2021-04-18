import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)

def msg_generator(msg):
    msg_list = msg.split(' ')
    if msg_list[0] == 'put':
        if msg_list[1] == 'ok_format_err':
            return 'sok\n\n'
        elif msg_list[1] == 'error_format_err':
            return 'serror\n\n'
        elif msg_list[1] == 'ending_err':
            return 'ok\n'
        elif msg_list[1] == 'ok_err':
            return 'ok\nwrong or no method\n\n'
        elif msg_list[1] == 'error':
            return 'error\nwrong or no method\n\n'
        else:
            return 'ok\n\n'
    elif msg_list[0] == 'get':
        return ' '
    else:
        return 'error\nwrong or no method\n\n'
    
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        incoming_msg = ''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            incoming_msg = data.decode('utf8')
            print(repr(incoming_msg))
            outcoming_msg = msg_generator(incoming_msg)
            print(repr(outcoming_msg))
            conn.sendall(outcoming_msg.encode('utf8'))
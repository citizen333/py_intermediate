import socket
import time

class ClientError(Exception):
    
    def __init__(self, message):
        self.message = message
        
class Client:
    
    response_statuses = ('ok', 'error')
    
    def __init__(self, host, port, timeout = None):
        self._host = str(host)
        self._port = int(port)
        if timeout is not None:
            self._timeout = float(timeout)
        else:
            self._timeout = timeout
        self._sock = socket.create_connection((self._host, self._port), self._timeout)
        print('connection established')
        
    def close_connection(self):
        self._sock.close()
        print('connection closed')
        
    def put(self, metric, value, timestamp = int(time.time())):
        message = 'put ' + str(metric) + ' ' + str(value) + ' ' + str(int(timestamp)) + '\n'
        try:
            self._sock.sendall(message.encode('utf8'))
            print('data sent')
        except self._sock.timeout:
            raise ClientError('Send timeout')
        except self._sock.error as ex:
            raise ClientError("Send data error:", ex)
            
        response = ''
        while True:
            try:
                data = self._sock.recv(1024)
                if not data:
                    break
                response += data.decode('utf8')
            except self._sock.timeout:
                raise ClientError('Read timeout')
            except self._sock.error as ex:
                raise ClientError("Read data error:", ex)
        
        if not (
            response.startswith(Client.response_statuses)\
            and response.endswith('\n\n')
        ):
            raise ClientError('Invalid format of response. Response: ' + response)
        
        if response.startswith('ok'):
            if response != 'ok\n\n':
                raise ClientError('Invalid format of response. Response: ' + response)
        
        if response.startswith('error'):
            raise ClientError('Response with error. Error: ' + response[6:-2])
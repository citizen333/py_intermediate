import socket
import time

class ClientError(Exception):
    
    def __init__(self, message):
        self.message = message
        
class Client:
    
    in_message_statuses = ('ok\n', 'error\n')
    
    def __init__(self, host, port, timeout = None):
        self._host = str(host)
        self._port = int(port)
        if timeout is not None:
            self._timeout = float(timeout)
        else:
            self._timeout = timeout
        self._sock = socket.create_connection((self._host, self._port), self._timeout)
        print('connection established')
    
    def connect(self):
        self._sock = socket.create_connection((self._host, self._port), self._timeout)
        print('connection established')
        
    def close_connection(self):
        self._sock.close()
        print('connection closed')
        
    def _send_message(self, msg):
        try:
            self._sock.sendall(msg.encode('utf8'))
            print('data sent')
        except self._sock.timeout:
            raise ClientError('Send timeout')
        except self._sock.error as ex:
            raise ClientError("Send data error:", ex)
        
    def _receive_message(self):
        try:
            data = self._sock.recv(1024)
            return data.decode('utf8')
        except self._sock.timeout:
            raise ClientError('Read timeout')
        except self._sock.error as ex:
            raise ClientError("Read data error:", ex)
        
    def _isint(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def _isfloat(self, value):
        try:
            float(value)
            return True
        except:
            return False
        
    def put(self, metric, value, timestamp = None):
        if timestamp is None:
            timestamp = int(time.time())
        out_message = 'put ' + str(metric) + ' ' + str(value) + ' ' + str(int(timestamp)) + '\n'
        self._send_message(out_message)
        in_message = self._receive_message()
        
        if not (
            in_message.startswith(Client.in_message_statuses)\
            and in_message.endswith('\n\n')
        ):
            raise ClientError('Invalid format of incoming message. Message: ' + repr(in_message))
        
        if in_message.startswith('ok\n'):
            if in_message != 'ok\n\n':
                raise ClientError('Invalid format of incoming message. Message: ' + repr(in_message))
        
        if in_message.startswith('error\n'):
            raise ClientError('Incoming message with error. Error: ' + in_message[6:-2])
        
    def get(self, metric):
        out_message = 'get ' + str(metric) + '\n'
        self._send_message(out_message)
        in_message = self._receive_message()
        
        if not (
            in_message.startswith(Client.in_message_statuses)\
            and in_message.endswith('\n\n')
        ):
            raise ClientError('Invalid format of incoming message. Message: ' + repr(in_message))
        
        if in_message.startswith('ok\n'):
            if in_message == 'ok\n\n':
                return {}
            else:
                result = {}
                for metric in in_message[3:-2].split('\n'):
                    metric_list = metric.split(' ')
                    if len(metric_list) != 3:
                        raise ClientError('Invalid format of metrics. Message: ' + repr(in_message))
                    elif not self._isint(metric_list[2]):
                        raise ClientError('Invalid format of timestamp. Message: ' + repr(in_message))
                    elif not self._isfloat(metric_list[1]):
                        raise ClientError('Invalid format of metric value. Message: ' + repr(in_message))
                    else:
                        result.setdefault(metric_list[0], [])
                        result[metric_list[0]].append((int(metric_list[2]), float(metric_list[1])))
                for key in result:
                    result[key].sort(key = lambda tup: tup[0])
                return result
        
        if in_message.startswith('error\n'):
            raise ClientError('Incoming message with error. Error: ' + in_message[6:-2])
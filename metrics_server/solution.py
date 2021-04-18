import asyncio

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)

class ClientServerProtocol(asyncio.Protocol):
    def __init__(self, metrics_storage):
        self.metrics = metrics_storage
        print("protocol initialized")
        
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}')
        self.transport = transport

    def data_received(self, data):
        in_message = data.decode('utf8')
        print(f'Got message {repr(in_message)}\
            of length {len(in_message)}'
            )
        out_message = self.process_data(in_message)
        print(
            f'Sending message {repr(out_message)}\
            of length {len(out_message)}'
        )
        self.transport.write(out_message.encode('utf8'))

    def process_data(self, data):
        if not (
            data.startswith(('put ', 'get '))\
            and data.endswith('\n')
        ):
            return self.error_wrapper('wrong command')
        
        if data.startswith('put '):
            payload = data[4:-1].split(' ')
            if len(payload) != 3:
                return self.error_wrapper('wrong command')
            if not self._isint(payload[-1]):
                return self.error_wrapper('wrong command')
            if not self._isfloat(payload[-2]):
                return self.error_wrapper('wrong command')
            metric = payload[0]
            timestamp = int(payload[2])
            value = float(payload[1])
            self.metrics.setdefault(metric, {timestamp: None})
            self.metrics[metric][timestamp] = float(value)
            print(self.metrics)
            return self.ok_wrapper('')
        
        if data.startswith('get '):
            payload = data[4:-1]
            
            if len(payload.split(' ')) != 1:
                return self.error_wrapper('wrong command')
            
            if len(self.metrics) == 0:
                return self.ok_wrapper('')
            
            message = ''
            if payload == '*':
                for metric in self.metrics:
                    for timestamp, value in self.metrics[metric].items():
                        message +=\
                            '\n' + str(metric) + ' '\
                            + str(value) + ' ' + str(timestamp)
            
            if payload in self.metrics.keys():
                for timestamp, value in self.metrics[payload].items():
                    message +=\
                        '\n' + str(payload) + ' '\
                        + str(value) + ' ' + str(timestamp)
            
            return self.ok_wrapper(message)
            
    
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
        
    def error_wrapper(self, message):
        return 'error\n' + str(message) + '\n\n'
    
    def ok_wrapper(self, message):
        return 'ok' + str(message) + '\n\n'

def run_server(host, port):
    metrics_storage = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        lambda: ClientServerProtocol(metrics_storage),
        host, port
    )

    server = loop.run_until_complete(coro)

    print(f'Serving on {server.sockets[0].getsockname()}')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('Server shut down')
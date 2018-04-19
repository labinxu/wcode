import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self,transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received:{!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'hello world'
import pdb; pdb.set_trace()
coro = loop.create_connection(lambda:EchoClientProtocol(message, loop),
                              host='127.0.0.1' ,port=8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()

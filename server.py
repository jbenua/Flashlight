from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from struct import *

define('port', default=9999, help="TCP port to use")


ON = b"\x12\x00\x00"
OFF = b"\x13\x00\x00"


class FlashlightServer(TCPServer):
    """Tornado asynchronous flashlight TCP server."""
    clients = set()

    def decode_data(self, data):
        if "on" in data:
            text = ON
        elif "off" in data:
            text = OFF
        elif 'color' in data:
            color = [int(c) for c in data.split(' ')[1:]]
            text = pack(">ch", b"\x20", 3)
            for component in color:
                text += pack(">B", component)
        else:
            text = data.encode()
        return text

    @gen.coroutine
    def handle_stream(self, stream, address):
        ip, fileno = address
        print("Incoming connection from " + ip)
        FlashlightServer.clients.add(address)
        print("Command examples:\n" +
            "'on'\n'off'\n'color 200 150 3'")
        while True:
            try:
                data = self.decode_data(input('(command) '))
                yield stream.write(data)
                print("Sending to client: ", data[:-1])
            except StreamClosedError:
                print("Client " + str(address) + " left, cannot send message.")
                FlashlightServer.clients.remove(address)
                break

if __name__ == "__main__":
    options.parse_command_line()
    server = FlashlightServer()
    server.listen(options.port)
    print("Starting server on tcp://localhost:" + str(options.port))

    IOLoop.current().start()

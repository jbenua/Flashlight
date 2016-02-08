from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import gen
from tornado.tcpclient import TCPClient
from struct import *
from controller import FlashlightController
from views.console_view import ConsoleView
from tornado.iostream import StreamClosedError

define('port', default=9999, help="TCP port to use")


class FlashlightClient():

    def __init__(self):
        self.controller = FlashlightController(ConsoleView())

    @gen.coroutine
    def run_client(self):
        """Setup the connection to the flashlight server and wait for user
        input.
        """
        stream = yield TCPClient().connect('127.0.0.1', options.port)
        try:
            while True:
                if not (yield self.flashlight(stream)):
                    break
        except KeyboardInterrupt:
            stream.close()

    @gen.coroutine
    def flashlight(self, stream):
        try:
            data = yield stream.read_until('\n'.encode())
        except StreamClosedError:
            print("Server closed connection")
            raise gen.Return(False)
        self.controller.execute_tlv(data)
        raise gen.Return(True)

if __name__ == "__main__":
    options.parse_command_line()
    print("Starting client...")
    client = FlashlightClient()
    IOLoop.instance().run_sync(client.run_client)

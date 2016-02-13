from tornado import gen, ioloop
from tornado.tcpclient import TCPClient
from controller import FlashlightController
from tornado.iostream import StreamClosedError


class FlashlightClient():

    def __init__(self, queue, client=None, port=9999):
        self.queue = queue
        self.stream = None
        self.port = port
        self.ws_client = client
        self.controller = FlashlightController(client)

    @gen.coroutine
    def connect(self):
        self.stream = yield TCPClient().connect('127.0.0.1', self.port)

    @gen.coroutine
    def close_connection(self):
        self.stream.close()

    @gen.coroutine
    def flashlight(self):
        try:
            data = yield self.controller.parse_stream(self.stream)
            if data:
                self.queue.put((data, self.ws_client))
        except StreamClosedError:
            print("Server closed connection")
            raise gen.Return(False)
        ioloop.IOLoop.current().spawn_callback(self.flashlight)
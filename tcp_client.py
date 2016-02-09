from tornado import gen, ioloop
from tornado.tcpclient import TCPClient
from controller import FlashlightController
# from views.console_view import ConsoleView
from tornado.iostream import StreamClosedError


class FlashlightClient():

    def __init__(self, queue, client=None, port=9999):
        self.queue = queue
        self.stream = None
        self.port = port
        #
        self.ws_client = client
        self.controller = FlashlightController(client)
        # Console_view() if console else WS

    @gen.coroutine
    def connect(self):
        self.stream = yield TCPClient().connect('127.0.0.1', self.port)

    # @gen.coroutine
    # def run_client(self):
    #     """wait for user input"""
    #     # try:
    #     while True:
    #         if not (yield self.flashlight()):
    #             break
    #     # except KeyboardInterrupt:
    #     #     yield self.close_connection()

    @gen.coroutine
    def close_connection(self):
        self.stream.close()

    @gen.coroutine
    def flashlight(self):
        try:
            data = yield self.stream.read_until('\n'.encode())
        except StreamClosedError:
            print("Server closed connection")
            raise gen.Return(False)
        # self.controller.execute_tlv(data)
        seq = self.controller.get_sequence(data)
        for command in seq:
            self.queue.put((command, self.ws_client))
        ioloop.IOLoop.current().spawn_callback(self.flashlight)
        raise gen.Return(True)

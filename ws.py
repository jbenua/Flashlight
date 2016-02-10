from tornado import websocket, ioloop, gen
from tcp_client import FlashlightClient


class EchoWebSocket(websocket.WebSocketHandler):

    @gen.coroutine
    def open(self):
        print("WebSocket opened")
        port = self.settings['port']
        queue = self.settings['commands_queue']
        self.tcp_client = FlashlightClient(queue, client=self, port=port)
        yield self.tcp_client.connect()
        ioloop.IOLoop.current().spawn_callback(self.tcp_client.flashlight)
        self.write_message("tcp opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
        if self.tcp_client.stream:
            self.tcp_client.close_connection()

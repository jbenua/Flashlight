from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import web
from struct import *
from ws import EchoWebSocket
import os
from command_worker import CommandQueue
from views.console_view import ConsoleView
from tcp_client import FlashlightClient


define('port', default=9999, help="TCP port to use")
define('console', default=False, help="Use console view")

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,)


class MainHandler(web.RequestHandler):
    def get(self):
        self.render('flashlight.html')


def web_view():
    app = web.Application(
        [(r'/', MainHandler),
        (r'/ws', EchoWebSocket)],
        **settings)
    app.listen(8888)
    app.settings['port'] = options.port
    app.settings['commands_queue'] = CommandQueue()
    IOLoop.current().spawn_callback(
        app.settings['commands_queue'].process_command)
    IOLoop.current().start()


def console_only():
    queue = CommandQueue()
    console_view = ConsoleView()
    client = FlashlightClient(
        queue, console_view, options.port)
    IOLoop.current().spawn_callback(
        queue.process_command)
    IOLoop.current().run_sync(client.connect)
    console_view.write_message("tcp opened")
    IOLoop.current().spawn_callback(client.flashlight)
    IOLoop.current().start()


if __name__ == "__main__":
    options.parse_command_line()
    print(options.console)
    print("Starting client...")
    if options.console:
        console_only()
    else:
        web_view()

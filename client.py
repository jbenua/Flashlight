from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado import web
from struct import *
from ws import EchoWebSocket
import os
from command_worker import CommandQueue


define('port', default=9999, help="TCP port to use")
define('console', default=True, help="Use console view")

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,)


class MainHandler(web.RequestHandler):
    def get(self):
        self.render('flashlight.html')

if __name__ == "__main__":
    options.parse_command_line()
    print(options.console)
    print("Starting client...")
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

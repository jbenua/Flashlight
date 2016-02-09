from ..command_worker import CommandQueue
from tornado.testing import gen_test
import tornado


class TestQueue(tornado.testing.AsyncTestCase):

    class DummyView():
        def __init__(self):
            self.commands = []

        def write_message(self, message):
            self.commands.append(message)

    class DummyServer():
        def __init__(self, queue):
            self.queue = queue

        def enqueue_command(self, command):
            self.queue.put(command)

    def setUp(self):
        super().setUp()
        self.view = TestQueue.DummyView()
        self.queue = CommandQueue()
        self.server = TestQueue.DummyServer(self.queue)
        tornado.ioloop.IOLoop.current().spawn_callback(
            self.queue.process_command)

    @gen_test
    def test_queue(self):
        item = (('command', None), self.view)
        self.server.enqueue_command(item)
        yield tornado.gen.sleep(0.15)
        self.assertNotEqual(self.view.commands, [],
            msg="Didn't receive command")
        self.assertEqual(self.queue.queue.qsize(), 0,
            msg="Item remains in the queue")

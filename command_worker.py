from tornado.queues import Queue
from tornado import gen


class CommandQueue():
    def __init__(self):
        self.queue = Queue()

    @gen.coroutine
    def process_command(self):
        while True:
            item = yield self.queue.get()
            try:
                yield gen.sleep(0.1)
                command, view = item
                print(command)
                view.write_message({command[0]: command[1]})
            finally:
                self.queue.task_done()

    def put(self, item):
        self.queue.put(item)

import os
import threading
import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient
import tornado.web
from tornado import gen
from tornado.web import asynchronous
from queue import Queue
import time

tornado.options.define('port', type=int, default=8888, help='server port number (default: 8888)')
tornado.options.define('debug', type=bool, default=False, help='run in debug mode with autoreload (default: False)')

class Scheduler():

    def __init__(self):
        self.ip_queue = Queue()
        self.ip_queue.put('posada1')
        self.ip_queue.put('posada2')
        self.ip_queue.put('posada3')

        self.list_lock = threading.RLock()

    def run(self, s, callback):
        ip_loc = None
        with self.list_lock:
            ip_loc = self.ip_queue.get()
        time.sleep(10)
        self.ip_queue.put(ip_loc)
        callback("IP Location should be " + ip_loc)

scheduler = Scheduler()

class Handler(tornado.web.RequestHandler):
    
    def other_call(self, s, callback):
        import time
        time.sleep(10)
        callback("String was " + s)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        response = yield tornado.gen.Task(scheduler.run, "Howdy")
        self.write(response)
        self.finish()

        # self.write("Hello World")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", Handler),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

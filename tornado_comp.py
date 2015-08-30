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
from cache import lru_cache

tornado.options.define('port', type=int, default=8888, help='server port number (default: 8888)')
tornado.options.define('debug', type=bool, default=False, help='run in debug mode with autoreload (default: False)')

@lru_cache(maxsize=10)
def client_api(parameter):

    if parameter == 10:
        client_api.clear()
        squares.clear()
        
        return "Square cleared"

    sq = squares(parameter)
    cb = cube(parameter)
    qu = quad(parameter)
    return sq+cb+qu

@lru_cache(maxsize=10)
def squares(num):
    print("Working on square for ", num)
    return num * num

@lru_cache(maxsize=10)
def cube(num):
    print("Working on cube for ", num)
    return num * num * num

@lru_cache(maxsize=10)
def quad(num):
    print("Working on quad for ", num)
    return num * num * num * num

class Scheduler():

    def __init__(self):
        self.ip_queue = Queue()
        self.ip_queue.put('posada1')
        self.ip_queue.put('posada2')
        self.ip_queue.put('posada3')

        self.list_lock = threading.RLock()

    def run(self, s, callback):
        retVal = client_api(int(s))
        callback(retVal)

scheduler = Scheduler()

class Handler(tornado.web.RequestHandler):
    
    def other_call(self, s, callback):
        import time
        time.sleep(10)
        callback("String was " + s)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        value=self.get_argument("val", 0, True)
        response = yield tornado.gen.Task(scheduler.run, value)
        print("Final Response was ", response)

        self.write(str(response))
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

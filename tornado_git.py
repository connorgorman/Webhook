import os
import threading
import time
import json
import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient
import tornado.web
from tornado import gen
from tornado.web import asynchronous

tornado.options.define('port', type=int, default=9000, help='server port number (default: 8888)')
tornado.options.define('debug', type=bool, default=False, help='run in debug mode with autoreload (default: False)')

class Handler(tornado.web.RequestHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        print(self.request.body)
        self.finish()

    @tornado.gen.engine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        self.finish()



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/postreceive", Handler),
            (r"/startup", Handler),
        ]
        settings = dict(
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug = tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    print("Server Booted")
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

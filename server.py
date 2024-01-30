#! /usr/bin/python
import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import asyncio
from tornado_request_mapping import request_mapping, Route

####### Serveur Tornado #######
PORT = 8443
settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static")
    )    

@request_mapping("/products")
class PainMainHandler(tornado.web.RequestHandler):
    @request_mapping("/order.html")
    def get(self):
        print("[HTTP](MainHandler) User Connected.")
        self.render("products/order.html")

@request_mapping("/ws")
class PainWSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('[WS] Connection was opened.')
 
    async def on_message(self, message):
        print('[WS] Incoming message:', message)

    def on_close(self):
        print('[WS] Connection was closed.')

if __name__ == "__main__":
    try:
        application = tornado.web.Application(**settings)
        route = Route(application)
        route.register(PainMainHandler)
        route.register(PainWSHandler)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()

        print("Tornado Server started")
        main_loop.start()
    
    except:
        print("Exception triggered - Tornado Server stopped.")

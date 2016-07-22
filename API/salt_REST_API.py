'''
note: python 2.6  2.7  not python 3
'''
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.autoreload
import salt.client


settings = {'debug': True}

class Server_Info_Handler(tornado.web.RequestHandler):
    def get(self):
        client = salt.client.LocalClient()
        response = client.cmd('*', 'grains.item',['nodename','ip4_interfaces:eth0','os', 'osrelease', 'osarch', 'num_cpus', 'cpu_model', 'cpuarch', 'virtual','mem_total'])
        self.write(response)

def make_app():
    return tornado.web.Application([
        (r"/server_info", Server_Info_Handler),
    ], **settings)

if __name__ == "__main__":
    try:
        print "Start the echo service"
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print "\nStop the echo service"

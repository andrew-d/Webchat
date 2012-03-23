import tornado.web
import tornadio2


class ChatConnection(tornadio2.SocketConnection):
    def on_message(self, message):
        print "I got a message:", message



socket_router = tornadio2.TornadioRouter(ChatConnection)


application = tornado.web.application(socket_router,
                    socket_io_port=8000)


if __name__ == "__main__":
    server = tornadio2.SocketServer(application)

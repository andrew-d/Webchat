import tornado.web
import tornadio2
from tornadio2 import event


class ChatController(object):
    def __init__(self):
        self.clients = []

    def new_client(self, client):
        self.clients.append(client)
        # TODO: Broadcast "blah joined the room" message

    def on_message(self, user, message):
        print "on_message:", message
        for c in self.clients:
            print "Sending message to:", repr(c)
            c.emit("chat_message", text=message, user=user)

    @staticmethod
    def instance():
        if not hasattr(ChatController, "_instance"):
            ChatController._instance = ChatController()
        return ChatController._instance


class ChatConnection(tornadio2.SocketConnection):
    def __init__(self, endpoint=None):
        self.controller = ChatController.instance()
        print "ChatConnection initialized:", repr(self), repr(endpoint)
        super(ChatConnection, self).__init__(endpoint)

    #def on_message(self, message):
    #    print "I got a message:", message
    #    self.controller.on_message(message)

    @event
    def message(self, message, user):
        print 'User: %s, Message: %s' % (user, message)
        self.controller.on_message(user, message)

    def on_open(self, request):
        print "Got new connection:", repr(request)
        self.controller.new_client(self)


socket_router = tornadio2.TornadioRouter(ChatConnection)
other_urls = [
    (r"/chat/(.*)", tornado.web.StaticFileHandler, {"path": "H:\\Profiles\\Andrew\\Documents\\Code\\Stripe\\WebChat\\frontend\\"}),
]

application = tornado.web.Application(
                    socket_router.apply_routes(other_urls),
                    socket_io_port=8000
            )


if __name__ == "__main__":
    print "Starting server..."
    server = tornadio2.SocketServer(application)

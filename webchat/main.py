import tornado.web
import tornadio2
from tornadio2 import event

DISTINGUISHED_USERS = {
    "admin": "admin",
    "andrew": "dunham",
    "asf": "stripe",
}


class ChatController(object):
    def __init__(self):
        self.clients_user = {}
        self.clients_conn = {}

    def new_client(self, client):
        print "Client connected:", repr(client)

    def _send_impl(self, conn, message, from_user, to_user):
        if from_user in DISTINGUISHED_USERS:
            from_user += "*"
        conn.emit("chat_message", text=message, from_user=from_user)

    def send_message(self, to_user, message):
        pass

    def on_message(self, connection, message):
        from_user = self.clients_conn[connection]

        for to_user, client in self.clients_user.iteritems():
            print "Sending message to:", to_user
            self._send_impl(client, message, from_user, to_user)

    def on_privmsg(self, connection, to_user, message):
        from_user = self.clients_conn[connection]

        try:
            to_user_conn = self.clients_user[to_user]
        except KeyError:
            print "Private message to user '%s' not deliverable!" % (to_user,)
            return

        self._send_impl(to_user_conn, message, from_user, to_user)

    def on_connect(self, connection, username, password):
        if username in DISTINGUISHED_USERS and not password == DISTINGUISHED_USERS[username]:
            self._send_impl(connection, "Error: '%s' is a reserved username, please pick another!" % (username,), "admin", "foobar")
        else:
            username = username.replace('*', '')
            self.clients_user[username] = connection
            self.clients_conn[connection] = username

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

    @event
    def message(self, message):
        #print 'User: %s, Message: %s' % (user, message)
        self.controller.on_message(self, message)

    @event
    def connected(self, username, password):
        self.controller.on_connect(self, username, password)

    @event
    def privmsg(self, to_user, message):
        self.controller.on_privmsg(self, to_user, message)

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

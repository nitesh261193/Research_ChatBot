import tornado.ioloop
import tornado.web
import tornado.websocket

import feedback
import chat


CHAT_GEN = chat.chat()

class Hello(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message("Hello, world")

    def on_message(self, message):
        if message == 'stop':
            Hello.on_close()
        next(CHAT_GEN)
        self.write_message(CHAT_GEN.send(message))

    def on_close(self):
        pass


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.write('''
<script>
ws = new WebSocket("ws://localhost:8888/websocket");
ws.onmessage = function(e) {
    alert('message received: ' + e.data);
};
</script>''')


application = tornado.web.Application([
    (r"/", Main),
    (r"/websocket", Hello),
])

if __name__ == "__main__":
    feedback.improve_using_feedback()
    next(CHAT_GEN)
    print("Initial request:", CHAT_GEN.send('Hi'))
    print("Goint to start server at port: 8888")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

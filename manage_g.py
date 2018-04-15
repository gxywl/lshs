from gevent.wsgi import WSGIServer
from manage import app

server = WSGIServer(('',8080), app)
server.serve_forever()
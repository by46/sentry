from .globals import _app_ctx_stack


class AppContext(object):
    def __init__(self, app):
        self.app = app

    def push(self):
        _app_ctx_stack.push(self)


class RequestContext(object):
    def __init__(self, app, socket, address):
        self.app = app
        self.request = app.request_class(socket, address)

    def push(self):
        _app_ctx_stack.push(self)

    def pop(self):
        _app_ctx_stack.pop()

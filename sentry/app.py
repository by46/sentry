import time
from threading import Lock

import six
from flask import Config
from flask.helpers import get_root_path
from gevent.server import StreamServer
from werkzeug.datastructures import ImmutableDict

from .config import ConfigAttribute
from .context import AppContext
from .context import RequestContext
from .map import Map
from .request import Request
from .rule import Rule

__version__ = '0.0.1'

_logger_lock = Lock()


class Sentry(object):
    action_key = 'request'
    config_class = Config

    default_config = ImmutableDict([
        ('DEBUG', False),
        ('SENTRY_HOST', '127.0.0.1'),
        ('SENTRY_PORT', 8081),
        ('LOGGER_NAME', 'None')
    ])

    rules = {}

    request_class = Request

    #: The rule object to use for payload rules created
    rule_class = Rule

    logger_name = ConfigAttribute('LOGGER_NAME')
    debug = ConfigAttribute('DEBUG')

    def __init__(self, import_name, root_path=None):
        self.import_name = import_name
        if root_path is None:
            root_path = get_root_path(import_name)
        self.root_path = root_path
        self.config = self.make_config()
        self.rule_map = Map()
        self._logger = None

    def make_config(self):
        root_path = self.root_path
        return self.config_class(root_path, self.default_config)

    def tcp_app(self, socket, address):
        start_point = time.time()
        ctx = self.request_context(socket, address)
        ctx.push()
        try:
            handle = self.rule_map.match(ctx.request)
            if handle:
                response = handle.dispatch()
                socket.sendall(response)
        finally:
            ctx.pop()
            self.logger.error('elapse %s', time.time() - start_point)

    def run(self, host=None, port=None, debug=None):
        if host is None:
            host = '127.0.0.1'
        if port is None:
            port = 80

        if debug is not None:
            self.debug = bool(debug)

        server = StreamServer((host, port), self.tcp_app)
        server.serve_forever()

    def route(self, action, **options):
        """

        :param action:
        :param options:
             override=False
        :return:
        """

        def decorator(f):
            self.add_rule(action, f, **options)
            return f

        return decorator

    def add_rule(self, action, f, **options):
        rule = self.rule_class(action, f)
        override = options.get('override')
        self.rule_map.add(rule, override)

    def register_blueprint(self, bp, override=False):
        for action, request_handler in six.iteritems(bp.rules):
            self.route(action, override=override)(request_handler)

    @property
    def logger(self):
        if self._logger and self._logger.name == self.logger_name:
            return self._logger
        with _logger_lock:
            if self._logger and self._logger.name == self.logger_name:
                return self._logger
            from sentry.logging import create_logger
            self._logger = rv = create_logger(self)
        return rv

    def app_context(self):
        return AppContext(self)

    def request_context(self, socket, address):
        return RequestContext(self, socket, address)

    def __call__(self, listener, client, address):
        return self.tcp_app(client, address)

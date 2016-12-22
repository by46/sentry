import json

from .zabbix import send_data


class BaseRequestHandler(object):
    def __init__(self, request):
        self.request = request

    def dispatch(self):
        response = self.handle(self.request)
        return self.make_response(response)

    @staticmethod
    def make_response(response):
        data = json.dumps(response)
        return send_data(data)

    def handle(self, request):
        """

        :param request:
        :return: json dict
        """
        return request


class DefaultRequestHandler(BaseRequestHandler):
    def handle(self, request):
        return {'response': 'success'}

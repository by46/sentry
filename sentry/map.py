class Map(object):
    def __init__(self):
        self._rules = []

    def add(self, rule, override=False):
        # TODO(benjamin): process duplicate
        self._rules.append(rule)

    def match(self, request):
        """

        :param request:
        :return: request handle
        """
        for rule in self._rules:
            if rule.match(request):
                return rule.handle_class(request)
        return None

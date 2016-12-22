class Rule(object):
    def __init__(self, action, handle_class, **options):
        self.action = action
        self.handle_class = handle_class
        self.options = options

    def match(self, request):
        raise NotImplementedError

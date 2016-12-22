class Blueprint(object):
    rules = {}

    def route(self, action):
        def decorator(f):
            self.rules[action] = f
            return f

        return decorator

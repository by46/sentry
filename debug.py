from sentry import Sentry

if __name__ == '__main__':
    worker = Sentry(__name__)
    worker.run('localhost', 8083, debug=True)

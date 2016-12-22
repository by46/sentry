class SentryException(Exception):
    """Sentry Base Exception

    """


class InvalidZabbixHeaderException(SentryException):
    """invalid zabbix header raise this exception

    """

    def __init__(self, message):
        message = 'Invalid zabbix header, actual data : {0}'.format(message)
        super(InvalidZabbixHeaderException, self).__init__(message)


class InvalidZabbixDataException(SentryException):
    def __init__(self, expect_length, actual_length):
        message = 'Expect data length: {0}, actual data length:{1}'.format(expect_length, actual_length)
        super(InvalidZabbixDataException, self).__init__(message)

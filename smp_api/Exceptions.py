class ExceptionWithMessage(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class InvalidUrl(Exception):
    pass


class OldChache(Exception):
    pass


class WebSiteBlocked(Exception):
    pass


class ErrorAtGettingPage(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class BadConfigurated(Exception):
    pass


class TwitterProfileNotFound(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


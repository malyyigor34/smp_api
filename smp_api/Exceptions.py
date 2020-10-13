class InvalidUrl(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

class OldChache(Exception):
    pass

class WebSiteBlocked(Exception):
    pass

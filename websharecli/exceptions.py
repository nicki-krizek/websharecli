class WebshareCliException(Exception):
    pass


class LinkUnavailableException(WebshareCliException):
    pass


class NotVipLinkException(WebshareCliException):
    pass


class InvalidUrlException(WebshareCliException):
    pass


class TooManyDownloadRetriesException(WebshareCliException):
    pass

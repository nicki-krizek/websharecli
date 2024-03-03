class WebshareCliException(Exception):
    pass


class LinkUnavailableException(WebshareCliException):
    pass


class NotVipLinkException(WebshareCliException):
    pass

import sys


class NullCallableString(str):
    """
    This emulates blessings class for cases when blessings aren't available
    """
    def __new__(cls):
        return str.__new__(cls, '')

    def __call__(self, arg, *extra_args):
        if isinstance(arg, int):
            return ''
        return arg


class PlainTerminal:
    """
    Mock of blessings Terminal that ignores formatting
    """
    nullstr = NullCallableString()

    def __getattr__(self, attr):
        setattr(self, attr, self.nullstr)
        return self.nullstr


COLOR_TERMINAL = False
try:
    import blessings
    # this can throw _curses.error: setupterm: could not find terminal
    # better find out now
    blessings.Terminal()
    Terminal = blessings.Terminal
    COLOR_TERMINAL = True
except Exception:
    Terminal = PlainTerminal


T = Terminal(stream=sys.stderr)

SYMBOLS = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')


def bytes2human(n):
    """Convert n bytes to a human readable value of 4 characters."""
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    prefix = {}
    for i, s in enumerate(SYMBOLS):
        prefix[s] = 1 << i*10
    for symbol in reversed(SYMBOLS):
        value = float(n) / prefix[symbol]
        if value <= 999 and value > 0.9:
            if value <= 9.9:
                fmt = "{value:1.1f}{symbol}"
            else:
                fmt = "{value:3.0f}{symbol}"
            return fmt.format(value=value, symbol=symbol)

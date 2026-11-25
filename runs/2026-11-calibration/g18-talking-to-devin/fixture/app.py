def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return a minus b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError('multiply expects numbers')
    return a * b

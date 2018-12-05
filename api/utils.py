import math


def kformat(n):
    """
    number with K ending(social visualisation of numbers).
    :param n:
    :return:
    """
    if not n:
        return 0

    sign_coef = 1

    if n < 0:
        sign_coef = -1
        n = n * sign_coef

    digits = int(math.log(n, 10)+1)
    layer = int((digits - 1) / 3)

    if layer == 0:
        return n

    base_n = sign_coef * round(n / (10 ** (layer * 3)), 1)

    # cut tail if zero.
    if base_n.is_integer():
        base_n = int(base_n)

    # Todo million - 2 layers = M
    return str(base_n) + ('K'*layer)

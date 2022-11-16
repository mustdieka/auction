def check_int(st):
    try:
        int(st)
        return True
    except ValueError:
        return False


def check_float(st):
    try:
        float(st)
        return True
    except ValueError:
        return False

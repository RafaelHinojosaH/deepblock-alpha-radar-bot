def safe_div(a, b, default=0):
    try:
        return a / b if b else default
    except:
        return default


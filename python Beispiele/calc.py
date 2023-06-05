
def add(a,b):
    return a + b

def substract(a,b):
    return a - b

def divide(a,b):
    if b == 0:
        raise ValueError("durch 0 teilen nicht möglich")
    return a / b
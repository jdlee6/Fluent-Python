# example - code for a running average coroutine

def averager():
    total = 0.0
    count = 0
    average = None
    # This infinite loop means this coroutine will keep on accepting values and producing results as long as the caller sends them. This coroutine will only terminate when the caller calls .close() on it or when it's garbage collected because there are NO more references to it
    while True:
        # The "yield" statement here is used to suspend the coroutine, produce a result to the caller, and - later - to get a value sent by the caller to the coroutine, which resumes its infinite loop
        term = yield average
        total += term
        count += 1
        average = total/count
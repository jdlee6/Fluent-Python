# registration.py module

# registry will hold references to functions decorated by @register
registry = []

# register takes a function as argument
def register(func):
    # display what function is being decorated, for demonstration
    print(f'running register{func}')
    # include func in registry
    registry.append(func)
    # return func: we must return a function, here we return the same received as argument
    return func

# f1 and f2 are decorated by @register
@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

# f3 is NOT decorated
def f3():
    print('running f3()')

# main displays the registy, then calls f1(), f2(), f3()
def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

# main() is only invoked if registration.py runs as a script
if __name__ == "__main__":
    main()

# output:
# running register<function f1 at 0x7fe9e2f8ea60>
# running register<function f2 at 0x7fe9e2f8eae8>
# running main()
# registry -> [<function f1 at 0x7fe9e2f8ea60>, <function f2 at 0x7fe9e2f8eae8>]
# running f1()
# running f2()
# running f3()
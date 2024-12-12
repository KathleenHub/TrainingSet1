def announce(f):
    def wrapper():
        print("about to run function")
        f()
        print("Done with function")
    return wrapper

@announce
def hello():
    print("Hello, world!")

hello()
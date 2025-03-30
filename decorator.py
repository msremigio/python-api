def decorator(func):
    def wrapper():
        print(f"Executed before {func.__name__}.")
        func()
        print(f"Executed after {func.__name__}.")
    return wrapper

@decorator
def hello():
    print("Hello World!")

hello()
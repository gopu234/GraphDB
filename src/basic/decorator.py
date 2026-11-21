import random

def ranndomnumberGenerator(function):
    def wrapper():
        random_number = random.randint(100, 1000)
        function(random_number)
    return wrapper

@ranndomnumberGenerator
def functionA(num):
    print(f"Random number for functionA is: {num}")

@ranndomnumberGenerator
def functionB(num):
    print(f"Random number for functionB is: {num}")

@ranndomnumberGenerator
def functionC(num):
    print(f"Random number for functionC is: {num}")

functionA()
functionB()
functionC()
# encapsulation, inheritance,  polymorphism, Abstraction

class Account:

    def __init__(self,balance):
        self.__balance = balance

    def getBalance(self):
        print("In getBalance")
        return self.__balance

    def setBalance(self,balance):
        print("In setBalance")
        self.__balance = balance

    

class Animal:
    def __init__(self):
        pass
    def speak(self):
        print("Animal makes a sound")
    def move(self):
        print("Animal moves")
    def eat(self):
        print("Animal eats")
    
class Dog(Animal):
    def __init__(self):
        pass
    def speak(self):
        print("Dog barks")
    def move(self):
        print("Dog runs")
    def eat(self):
        super().eat()
        print("Dog eats")
    
d= Dog()
d.eat()  

#Abstract class


from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius * self.radius

class Square(Shape):
    def __init__(self,side):
        self.side = side
    def area(self):
        return self.side * self.side

c = Circle(5)
s = Square(5)
print(c.area())
print(s.area())
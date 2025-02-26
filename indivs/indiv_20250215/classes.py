
class Person:

    members = []

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Person.members.append(self)

    def __call__(self, *args, **kwargs):
        print(f"Hello, my name is {self.name}. I am {self.age} years old.")


    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


person1 = Person(name="John", age=25)
person2 = Person(name="Alua", age=25)
person3 = Person(name="Ulan", age=25)

print(person2.members)





class Contact:

    def __init__(self, new_name, new_number):  # constructor
        self.name = new_name
        self.number = new_number


contact_mama = Contact(new_name="Mama", new_number="+7 777 777 55 55")
contact_papa = Contact("Papa", "+7 777 777 99 99")

print(contact_mama)
print(contact_mama.name)
print(contact_mama.number)

print( type(contact_mama) )
print("========================")
print(contact_papa)
print( type(contact_papa) )





# a = "hello"
# b = 87
# c = [1, 4, 5, 6, "hahaha"]
#
# print( type(a) )
# print( type(b) )
# print( type(c) )


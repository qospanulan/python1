
# get_area()
# get_perimeter()

class Rectangle:

    def __init__(self, height, width):
        self.height = height
        self.width = width

    def get_area(self):
        area = self.height * self.width
        return area

    def get_perimeter(self):
        per = 2 * (self.height + self.width)
        return per


rec1 = Rectangle(height=5, width=4)
rec2 = Rectangle(height=30, width=7)

area = rec1.get_area()
per = rec1.get_perimeter()
print(f"Area of rectangle1 is {area}")
print(f"Perimeter of rectangle1 is {per}")

area = rec2.get_area()
per = rec2.get_perimeter()
print(f"Area of rectangle2 is {area}")
print(f"Perimeter of rectangle2 is {per}")

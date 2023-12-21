class Product:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height

    def __str__(self):
        return f"Product({self.length}, {self.width}, {self.height})"

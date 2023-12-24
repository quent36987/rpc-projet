class Product:
    def __init__(self, id, length, width, height, delivery_priority=-1):
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height
        self.delivery_priority = delivery_priority
        self.id = id

    def __str__(self):
        return f"Product(id:{self.id}, {self.length} x {self.width} x {self.height}, priority: {self.delivery_priority}"

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

    def is_smaller_than(self, truck):
        return (
        self.length <= truck.length and self.width <= truck.width and self.height <= truck.height
        or self.length <= truck.length and self.width <= truck.height and self.height <= truck.width
        or self.length <= truck.width and self.width <= truck.length and self.height <= truck.height
        or self.length <= truck.width and self.width <= truck.height and self.height <= truck.length
        or self.length <= truck.height and self.width <= truck.length and self.height <= truck.width
        or self.length <= truck.height and self.width <= truck.width and self.height <= truck.length
        )

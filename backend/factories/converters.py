class ProductTypeConverter:

    def __init__(self):
        self.regex = 'pipes|pumps|wagons|drills|storage-tanks'
        self.factory_types = {'drills': 1, 'pumps': 2, 'pipes': 3, 'wagons': 4, 'storage-tanks': 5}

    def to_python(self, value):
        return self.factory_types[value]

    def to_url(self, value):
        return value

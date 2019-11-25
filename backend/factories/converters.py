class ProductTypeConverter:
    regex = 'pipes|pumps|wagons|drills'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return value

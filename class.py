class Car:
    def __init__(self, manufacturer, model, year):
        self.manufacturer = manufacturer
        self.model = model
        self.year = year

bmw = Car('BMW', 'm3', 2019)
print(bmw)
print(bmw.manufacturer, bmw.model, bmw.year)

mercedes = Car('Mercedes', 'c180', 2018)
print(mercedes)
print(mercedes.manufacturer, mercedes.model, mercedes.year)
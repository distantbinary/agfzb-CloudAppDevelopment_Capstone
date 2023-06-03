from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Convertible', 'Convertible'),
        ('Wagon', 'Wagon'),
        ('Compact', 'Compact'),
    )

    name = models.CharField(max_length=250)
    dealer_id = models.IntegerField()   # to refer a dealer created in cloudant database
    type = models.CharField(max_length=100, choices=CAR_TYPES)
    year = models.DateField()
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
	    # Dealer st
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data

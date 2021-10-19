from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Location(models.Model):
    # name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=512)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def full_address(self):
        # return '{}, {}, {}, {}'.format(self.city.region.country.name, self.city.region.name, self.city.name, self.address)
        return '{}, {}'.format(self.city.name, self.address)

    def __str__(self):
        # return '{}, {}, {}, {}'.format(self.city.region.country.name, self.city.region.name, self.city.name, self.address)
        return '{}, {}'.format(self.city.name, self.address)


class Address(models.Model):
    street = models.CharField(max_length=150)
    house = models.CharField(max_length=50)
    apartment = models.CharField(max_length=50)
    floor = models.IntegerField()
    entrance = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_address") 
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.user.phone


class Storage_region(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

def outlet_logo_dir(instanse, filename):
    folder_name = f"{instanse.name}/{filename}"
    return folder_name
class Outlets(models.Model):
    logo = models.ImageField(upload_to=outlet_logo_dir, default="default/default.png")
    name = models.CharField(max_length = 300)
    phone = models.CharField(max_length = 12)
    credit = models.CharField(max_length = 300)
    paymets = models.IntegerField(default=0)
    galleon = models.BooleanField(default=True)
    debt = models.IntegerField(default=0)
    refion = models.ForeignKey(City, on_delete=models.CASCADE)
    agent = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.db import models
from django.conf import settings

class Address(models.Model):
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=30)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    zip = models.CharField(max_length=12)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '%s: %s' % (self.street, self.number)
    


class City(models.Model):
    """City model"""
    name = models.CharField(max_length=255)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class State(models.Model):
    """State model"""
    name = models.CharField(max_length=255)
    init = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    
from django.db import models

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name

class CarModel(models.Model):
    class Meta:
        # Each CarModel has to be totally unique
        unique_together = ("make", "name", "year")
    make = models.ForeignKey(CarMake)
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    def __unicode__(self):
        return '%s %s %s' % (self.year, self.make, self.name)

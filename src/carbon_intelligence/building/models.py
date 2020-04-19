from django.db import models

# Create your models here.


class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=63)

    # these are the transformations that would need to be applied to each column of data, in order, from the csv file.
    csv_transformations = [int, str]

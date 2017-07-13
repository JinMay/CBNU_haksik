from django.db import models

class Main(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day

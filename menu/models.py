from django.db import models

class Main(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day


class Yangsung(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day


class Yangjin(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day


class Crj(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day


class Galaxy(models.Model):
    day = models.TextField()

    def __str__(self):
        return self.day


class Star(models.Model):
    day = models.TextField()

    def __str__(self):
        return self.day


class Hanbit(models.Model):
    number = models.IntegerField()
    day = models.TextField()

    def __str__(self):
        return self.day

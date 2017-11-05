import random
from django.db import models


class PostOffice(models.Model):
    name = models.CharField(max_length=255)
    index = models.CharField(default=random.randint(100000, 999999), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Почтовый офис'
        verbose_name_plural = 'Почтовые офисы'


class Elevation(models.Model):
    TYPES = (
        ('in', 'In'),
        ('out', 'Out'),
    )
    post_office = models.ForeignKey(PostOffice)
    type = models.CharField(choices=TYPES, max_length=10)
    datetime = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "{}: {}".format(self.post_office.name, self.datetime)

    class Meta:
        ordering = ['datetime']
        verbose_name = 'Отметка в одтелении'
        verbose_name_plural = 'отметки в отделениях'


class Item(models.Model):
    STATUS_CHOICES = (
        ('Adopted at', 'Adopted at'),
        ('Treatment', 'Treatment'),
        ('En route', 'En route'),
        ('Awaits delivery', 'Awaits delivery'),
        ('Delivered', 'Delivered'),
    )
    CATEGORIES = (
        ('Letter', 'Letter'),
        ('Parcel post', 'Parcel post'),
        ('Small package', 'Small package'),
        ('Package', 'Package'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=255)
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    path = models.ManyToManyField(Elevation, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    category = models.CharField(choices=CATEGORIES, max_length=255)
    address_from = models.ForeignKey(PostOffice, verbose_name='from PostOffice', related_name='from_post_office')
    address_to = models.ForeignKey(PostOffice, verbose_name='to PostOffice', related_name='to_post_office')

    def add_to_path(self, elevation):
        self.path.add(elevation)

    def __str__(self):
        return self.name + ' from: ' + self.address_from.name + ', to: ' + self.address_to.name

    class Meta:
        verbose_name = 'Объект доставки'
        verbose_name_plural = 'Объекты доставки'

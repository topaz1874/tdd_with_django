from django.db import models

# Create your models here.


class Item(models.Model):
    text = models.TextField(default='')

    def __unicode__(self):
        return str(self.text)

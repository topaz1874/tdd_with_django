from django.db import models

# Create your models here.

class List(models.Model):
    pass

    
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    def __unicode__(self):
        return str(self.text)


from django.db import models
from manager.widgets import GoogleMapsWidget

class Node(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    longitude   = models.FloatField(blank=True, null=True)
    latitude    = models.FloatField(blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class DataStream(models.Model):
    label  = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.label

class DataPoint(models.Model):
    value   = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    
    node    = models.ForeignKey(Node)
    stream  = models.ForeignKey(DataStream)
    
    def __unicode__(self):
        return self.stream.label + ': ' + str(self.value) + ' ' + self.stream.symbol

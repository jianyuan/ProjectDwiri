from django.db import models
from manager.widgets import GoogleMapsWidget

class Node(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address     = models.IntegerField('Node address', unique=True)
    longitude   = models.FloatField(blank=True, null=True)
    latitude    = models.FloatField(blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class DataStream(models.Model):
    ANALOG_0 = 'analog_0'
    ANALOG_1 = 'analog_1'
    ANALOG_2 = 'analog_2'
    ANALOG_3 = 'analog_3'
    ANALOG_4 = 'analog_4'
    ANALOG_5 = 'analog_5'
    INPUT_CHOICES = (
        (ANALOG_0, 'Analog 0'),
        (ANALOG_1, 'Analog 1'),
        (ANALOG_2, 'Analog 2'),
        (ANALOG_3, 'Analog 3'),
        (ANALOG_4, 'Analog 4'),
        (ANALOG_5, 'Analog 5'),
    )
    inputpin = models.CharField('Input pin', max_length=50, unique=True, choices=INPUT_CHOICES)
    label    = models.CharField(max_length=50)
    symbol   = models.CharField(max_length=10)
    formula  = models.CharField('Python code (Use x for raw value)', max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return self.label

class DataPoint(models.Model):
    raw_value = models.FloatField()
    created   = models.DateTimeField(auto_now_add=True)
    
    node      = models.ForeignKey(Node)
    stream    = models.ForeignKey(DataStream)
    
    def _get_value(self):
        if not self.stream.formula:
            return self.raw_value

        try:
            return eval(self.stream.formula.replace('x', 'self.raw_value'))
        except SyntaxError:
            return self.raw_value

    value = property(_get_value)

    def __unicode__(self):
        return self.stream.label + ': ' + str(self.value) + ' ' + self.stream.symbol

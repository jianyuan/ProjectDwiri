from manager.models import Node, DataStream, DataPoint
from manager.widgets import GoogleMapsWidget
from django.contrib import admin
from django import forms

class NodeAdminForm(forms.ModelForm):

    latitude = forms.CharField(label='Location', widget=GoogleMapsWidget(
        attrs={'width': 800, 'height': 400, 'longitude_id': 'id_longitude', 'country_city': 'London, United Kingdom'}),
        error_messages={'required': 'Please select point from the map.'})
    longitude = forms.CharField(widget = forms.HiddenInput())

    class Meta:
        model = Node

class NodeAdmin(admin.ModelAdmin):
    form = NodeAdminForm

admin.site.register(Node, NodeAdmin)
admin.site.register(DataStream)
admin.site.register(DataPoint)

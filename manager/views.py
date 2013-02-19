from django.shortcuts import get_object_or_404, render, render_to_response
from manager.models import Node, DataStream, DataPoint

def home(request):
    nodes = Node.objects.all()
    return render(request, 'home.html', {'nodes': nodes})

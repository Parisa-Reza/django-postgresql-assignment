from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Location, Property
from  django.db.models import Q
from django.shortcuts import render, get_object_or_404

def home(request):
    # Fetch active geographic nodes 
    return render(request, 'property_app/home.html')


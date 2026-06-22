from django.core.paginator import Paginator
from .models import Location, Property
from  django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.measure import D                 
from django.contrib.gis.geos import Point

def home(request):
    # Fetch active geographic nodes 
    return render(request, 'property_app/home.html')

def property_listing(request):
    # Base query for all visible active property listings
    queryset = Property.objects.filter(is_active=True).order_by('-created_at')
    
    # Read the single search bar input from the request
    query = request.GET.get('q', '').strip()

    if query:
        # Spatial Search Check - Look for a matching Location entry by City or Country name
        matching_location = Location.objects.filter(
            Q(city__icontains=query) | Q(country__icontains=query), 
            is_active=True
        ).first()

        if matching_location and matching_location.point:
          
            queryset = queryset.filter(
                point__distance_lte=(matching_location.point, D(km=10))
            )
        else:
            # Fallback - Scan across property titles, descriptions, and related location attributes
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(location__city__icontains=query) |
                Q(location__country__icontains=query)
            )

    # Paginate results down to a layout size of 2 properties per page view
    paginator = Paginator(queryset, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'property_app/listing.html', {'page_obj': page_obj})



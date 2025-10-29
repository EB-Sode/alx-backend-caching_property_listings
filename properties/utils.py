from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check if data exists in cache
    properties = cache.get('all_properties')

    if properties is None:
        print("Fetching from database...")  # for debugging
        properties = list(Property.objects.values())
        # Cache the queryset for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    else:
        print("Fetching from cache...")  # for debugging

    return properties

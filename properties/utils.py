from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check if data exists in cache
    properties = cache.get('all_properties')

    if properties is None:
        print("Fetching from database...")
        properties = Property.objects.all().values()
        cache.set('all_properties', properties, 3600)
    else:
        print("Fetching from cache...")

    return properties

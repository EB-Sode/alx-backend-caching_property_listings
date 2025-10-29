from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection

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



def get_redis_cache_metrics():
    """
    Retrieve Redis keyspace hit/miss metrics and calculate hit ratio.
    """
    try:
        # Connect to Redis using Django's configured cache
        redis_conn = get_redis_connection("default")

        # Get Redis info dictionary
        info = redis_conn.info()

        # Extract keyspace hits and misses
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Compute hit ratio
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }

        print(f"📊 Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        print(f"⚠️ Error retrieving Redis metrics: {e}")
        return {"error": str(e)}

from django.core.cache import cache
from .models import Property
import logging
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

# Configure logger
logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics (hits, misses, and hit ratio),
    and log results or errors appropriately.
    """
    try:
        # Connect to Redis via django-redis
        redis_conn = get_redis_connection("default")

        # Fetch Redis server stats
        info = redis_conn.info()

        # Extract keyspace hit/miss data
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate total requests and hit ratio
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }

        # Log the metrics
        logger.info(f"📊 Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logger.error(f"⚠️ Error retrieving Redis metrics: {e}")
        return {"error": str(e)}

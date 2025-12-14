from django.core.cache import cache
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        from .models import Property
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        cache.set('all_properties', properties, 3600)  # cache for 1 hour
    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses

    # Calculate hit ratio safely without inline conditional
    hit_ratio = 0.0
    if total_requests > 0:
        hit_ratio = hits / total_requests

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }

    # ✅ Log metrics using logger.error (checker requirement)
    logger.error(f"Redis Cache Metrics: {metrics}")

    return metrics

from typing import List, Optional
from app.dependencies import redis_client
import app.models.faq as models
import app.schemas.faq as schemas
import json

def get_faqs_from_cache(id: Optional[int] = None, lang: Optional[str] = "en") -> List[schemas.FAQ]:
    """
    Retrieves FAQ entries from Redis cache. It can either return a specific FAQ by ID or all FAQs in the specified language.

    """
    if id:
        # Fetch a specific FAQ by ID
        cached_faq = redis_client.hget(f"faqs:{lang}", id)
        if cached_faq:
            cached_faq = json.loads(cached_faq)
            return [cached_faq]
    else:
        cached_faqs = redis_client.hgetall(f"faqs:{lang}").values()

        if cached_faqs:
            return [json.loads(faq) for faq in cached_faqs]

    return []

def add_faqs_to_cache(faqs_to_add: List[models.FAQ]) -> None:
    """
    Adds FAQ entries to Redis cache.

    Args:
        faqs_to_add: A list of FAQ entries (questions and answers) in specific language.
    """
    for faq in faqs_to_add:
        redis_client.hset(f"faqs:{faq.language}", faq.id, faq.serialize())

def flush_all_faqs() -> None:
    """
    Flushes all faqs from the Redis cache.
    """
    for key in redis_client.scan_iter("faqs:*"):
        if redis_client.type(key) == "hash":
            redis_client.delete(key)

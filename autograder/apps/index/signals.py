from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GraderUser
from ..rankings.tasks import update_codeforces_rating
import threading
import logging

logger = logging.getLogger(__name__)
_signal_lock = threading.local()


@receiver(post_save, sender=GraderUser)
def handle_user_updates(sender, instance, created, update_fields=None, **kwargs):
    if getattr(_signal_lock, "in_signal", False):
        return

    usaco_map = {
        "Not Participated": 800,
        "Bronze": 800,
        "Silver": 1200,
        "Gold": 1600,
        "Platinum": 1900,
    }

    new_usaco_rating = usaco_map.get(instance.usaco_division, 800)
    if instance.usaco_rating != new_usaco_rating:
        instance.usaco_rating = new_usaco_rating
        try:
            _signal_lock.in_signal = True
            instance.save(update_fields=["usaco_rating"])
        finally:
            _signal_lock.in_signal = False

    update_codeforces_rating.delay(instance.id)

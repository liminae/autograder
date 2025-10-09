import logging

logger = logging.getLogger(__name__)


def save_ion_profile_data(backend, user, details, *args, **kwargs):
    """
    Save extra fields from Ion (via 'details') to the custom user model.
    """
    if backend.name == "ion" and user is not None:
        user.grade = details.get("grade", user.grade).capitalize()
        user.save()

from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete
from moringaschool.models import Image

@receiver(post_delete, sender=Image)
def delete_associated_files(sender, instance, **kwargs):
    """Remove all files of an image after deletion."""
    path = instance.file.name
    if path:
        default_storage.delete(path)
    
    
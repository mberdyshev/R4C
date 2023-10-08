from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, dispatch_uid='validate_model')
def validate_model(sender, **kwargs):
    if kwargs['raw']:  # https://docs.djangoproject.com/en/4.2/topics/db/fixtures/#how-fixtures-are-saved-to-the-database
        return
    kwargs['instance'].full_clean()

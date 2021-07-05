from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Inspector, Admin, Supervisor

USER_KIND = User.UserKind


@receiver(post_save, sender=Inspector)
@receiver(post_save, sender=Admin)
@receiver(post_save, sender=Supervisor)
def do_something(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.user.id)

        if isinstance(instance, Inspector):
            user.kind = USER_KIND.INSPECTOR

        elif isinstance(instance, Supervisor):
            user.kind = USER_KIND.SUPERVISOR

        elif isinstance(instance, Admin):
            user.kind = USER_KIND.ADMIN

        user.save()

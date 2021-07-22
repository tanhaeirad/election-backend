from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Inspector, Admin, Supervisor

USER_KIND = User.UserKind


@receiver(post_save, sender=Inspector, dispatch_uid="post_save_inspector_change_kind_for_user")
@receiver(post_save, sender=Admin, dispatch_uid="post_save_admin_change_kind_for_user")
@receiver(post_save, sender=Supervisor, dispatch_uid="post_save_supervisor_change_kind_for_user")
def set_kind_for_user_post_save_signal(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.user.id)

        if isinstance(instance, Inspector):
            user.kind = USER_KIND.INSPECTOR

        elif isinstance(instance, Supervisor):
            user.kind = USER_KIND.SUPERVISOR

        elif isinstance(instance, Admin):
            user.kind = USER_KIND.ADMIN

        user.save()

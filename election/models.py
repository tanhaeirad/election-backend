from django.db import models
from django.utils.translation import gettext as _


class City(models.Model):
    name = models.CharField(max_length=255)


class Zone(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Election(models.Model):
    class ElectionStatus(models.TextChoices):
        PENDING_FOR_INSPECTOR = 'Pending For Inspector', _('Pending For Inspector')
        PENDING_FOR_SUPERVISOR = 'Pending For Supervisor', _('Pending For Supervisor')
        REJECTED = 'Rejected', _('Rejected')
        ACCEPTED = 'Accepted', _('Accepted')

    zone = models.OneToOneField(Zone, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=ElectionStatus.choices,
                              default=ElectionStatus.PENDING_FOR_INSPECTOR)


class Candidate(models.Model):
    class CandidateStatus(models.TextChoices):
        PENDING_FOR_INSPECTOR = 'Pending For Inspector', _('Pending For Inspector')
        PENDING_FOR_SUPERVISOR = 'Pending For Supervisor', _('Pending For Supervisor')
        REJECTED = 'Rejected', _('Rejected')
        ACCEPTED = 'Accepted', _('Accepted')

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    vote1 = models.IntegerField(null=True)
    vote2 = models.IntegerField(null=True)
    election = models.ForeignKey(to=Election, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=CandidateStatus.choices,
                              default=CandidateStatus.PENDING_FOR_INSPECTOR)

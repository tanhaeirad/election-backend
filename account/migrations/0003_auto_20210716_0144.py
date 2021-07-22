# Generated by Django 3.2.4 on 2021-07-16 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0004_candidate_election'),
        ('account', '0002_auto_20210711_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspector',
            name='zone',
        ),
        migrations.RemoveField(
            model_name='supervisor',
            name='zone',
        ),
        migrations.AddField(
            model_name='inspector',
            name='election',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='election.election'),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='election',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='election.election'),
        ),
    ]
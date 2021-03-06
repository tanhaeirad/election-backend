# Generated by Django 3.2.4 on 2021-07-16 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210716_0542'),
        ('election', '0004_candidate_election'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='inspector',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.inspector'),
        ),
        migrations.AddField(
            model_name='election',
            name='supervisor',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.supervisor'),
        ),
    ]

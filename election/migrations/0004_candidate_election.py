# Generated by Django 3.2.4 on 2021-07-14 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0003_alter_zone_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending For Inspector', 'Pending For Inspector'), ('Pending For Supervisor', 'Pending For Supervisor'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending For Inspector', max_length=255)),
                ('zone', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='election.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('vote1', models.IntegerField(null=True)),
                ('vote2', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('Pending For Inspector', 'Pending For Inspector'), ('Pending For Supervisor', 'Pending For Supervisor'), ('Rejected', 'Rejected'), ('Accepted', 'Accepted')], default='Pending For Inspector', max_length=255)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.election')),
            ],
        ),
    ]

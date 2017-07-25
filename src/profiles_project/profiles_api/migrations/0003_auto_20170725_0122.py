# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-25 01:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0002_profilefeeditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('notes', models.CharField(max_length=255)),
                ('price', models.FloatField(null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityPeopleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.ActivityData')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityTypeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('show_in_app', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChairsData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DevelopersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EventData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('event_image_url', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeopleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('birthdate', models.DateField()),
                ('photo', models.URLField()),
                ('resume', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.CreateModel(
            name='PeopleSocialNetworksData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PeopleData')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceCategoryData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('show_in_app', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('altitude', models.CharField(max_length=255)),
                ('indication', models.CharField(max_length=255)),
                ('additional_info', models.CharField(max_length=255)),
                ('website', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=20)),
                ('image', models.URLField()),
                ('place_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlaceCategoryData')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceSocialNetworksData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlaceData')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.CreateModel(
            name='SketchData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('description', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetworksData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('domain', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PeopleData')),
            ],
        ),
        migrations.CreateModel(
            name='StreamData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('description', models.CharField(max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData')),
            ],
        ),
        migrations.AddField(
            model_name='placesocialnetworksdata',
            name='social_networks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.SocialNetworksData'),
        ),
        migrations.AddField(
            model_name='peoplesocialnetworksdata',
            name='social_network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.SocialNetworksData'),
        ),
        migrations.AddField(
            model_name='peopledata',
            name='provenance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlaceData'),
        ),
        migrations.AddField(
            model_name='eventdata',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlaceData'),
        ),
        migrations.AddField(
            model_name='eventdata',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles_api.ScheduleData'),
        ),
        migrations.AddField(
            model_name='eventdata',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='developersdata',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData'),
        ),
        migrations.AddField(
            model_name='developersdata',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PeopleData'),
        ),
        migrations.AddField(
            model_name='chairsdata',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData'),
        ),
        migrations.AddField(
            model_name='chairsdata',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PeopleData'),
        ),
        migrations.AddField(
            model_name='activitytypedata',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.EventData'),
        ),
        migrations.AddField(
            model_name='activitypeopledata',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PeopleData'),
        ),
        migrations.AddField(
            model_name='activitydata',
            name='activity_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.ActivityTypeData'),
        ),
        migrations.AddField(
            model_name='activitydata',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.PlaceData'),
        ),
        migrations.AddField(
            model_name='activitydata',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles_api.ScheduleData'),
        ),
    ]

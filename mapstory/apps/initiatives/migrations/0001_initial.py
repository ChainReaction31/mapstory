# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mapstories', '0002_mapstory_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('layers', '24_to_26'),
        ('base_groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('basegroup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base_groups.BaseGroup')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, null=True, blank=True)),
                ('slogan', models.CharField(max_length=255)),
                ('about', models.TextField(default=b'')),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(default=b'', max_length=255)),
                ('country', models.CharField(default=b'', max_length=255)),
                ('image', models.ImageField(null=True, upload_to=b'initiatives', blank=True)),
            ],
            bases=('base_groups.basegroup',),
        ),
        migrations.CreateModel(
            name='InitiativeLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('initiative', models.ForeignKey(to='initiatives.Initiative')),
                ('layer', models.ForeignKey(to='layers.Layer')),
            ],
        ),
        migrations.CreateModel(
            name='InitiativeMapStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('initiative', models.ForeignKey(to='initiatives.Initiative')),
                ('mapstory', models.ForeignKey(to='mapstories.MapStory')),
            ],
        ),
        migrations.CreateModel(
            name='InitiativeMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_since', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('initiative', models.ForeignKey(to='initiatives.Initiative')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Memberships',
            },
        ),
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_open', models.BooleanField(default=True)),
                ('approved_by', models.ForeignKey(blank=True, to='initiatives.InitiativeMembership', null=True)),
                ('initiative', models.ForeignKey(to='initiatives.Initiative')),
                ('user', models.ForeignKey(related_name='initiatives_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='initiativemapstory',
            name='membership',
            field=models.ForeignKey(to='initiatives.InitiativeMembership'),
        ),
        migrations.AddField(
            model_name='initiativelayer',
            name='membership',
            field=models.ForeignKey(to='initiatives.InitiativeMembership'),
        ),
    ]

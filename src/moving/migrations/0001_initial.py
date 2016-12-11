# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('embed_code', models.CharField(max_length=200, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('free_preview', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MoveManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=5000, null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=b'images/', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(default=b'abc', unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='move',
            name='move_type',
            field=models.ForeignKey(to='moving.Type', null=True),
            preserve_default=True,
        ),
    ]

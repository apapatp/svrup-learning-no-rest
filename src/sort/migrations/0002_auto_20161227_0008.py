# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sort', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SortLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'location_name', max_length=255)),
                ('item', models.IntegerField(default=0, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=b'images/', blank=True)),
                ('slug', models.SlugField(default=b'room', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='sort',
            options={'ordering': ['area', 'timestamp']},
        ),
        migrations.AddField(
            model_name='sort',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sort',
            name='area',
            field=models.ForeignKey(related_name='sort_by_location', default=None, to='sort.SortLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sort',
            name='slug',
            field=models.SlugField(default=b'sort', unique=True),
            preserve_default=True,
        ),
    ]

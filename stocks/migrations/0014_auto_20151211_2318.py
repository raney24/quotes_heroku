# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0013_auto_20151211_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='earnings',
            name='projected_er_date',
        ),
        migrations.AddField(
            model_name='stock',
            name='projected_er_date',
            field=models.DateField(default=b'2000-1-1'),
        ),
    ]

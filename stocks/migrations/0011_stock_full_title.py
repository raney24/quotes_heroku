# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0010_auto_20151211_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='full_title',
            field=models.CharField(default=b'Unknown Stock', max_length=40, verbose_name=b'Stock Name'),
        ),
    ]

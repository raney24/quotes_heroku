# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0015_auto_20151216_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='aggressive',
            field=models.BooleanField(default=False),
        ),
    ]

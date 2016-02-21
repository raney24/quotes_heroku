# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0019_auto_20160112_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

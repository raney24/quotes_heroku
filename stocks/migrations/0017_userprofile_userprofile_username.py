# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0016_userprofile_aggressive'),
        (b'contenttypes', b'__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='userprofile_username',
            field=models.CharField(default=100, max_length=40),
            preserve_default=False,
        ),
    ]

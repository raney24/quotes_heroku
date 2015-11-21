# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_earnings_er_quarter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='er_date',
            field=models.DateField(),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0012_earnings_projected_er_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='projected_er_date',
            field=models.DateField(default=b'2000-1-1'),
        ),
    ]

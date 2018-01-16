# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='display_type',
            field=models.SmallIntegerField(verbose_name='展示类型', default=1, choices=[(0, '标题'), (1, '图片')]),
        ),
    ]

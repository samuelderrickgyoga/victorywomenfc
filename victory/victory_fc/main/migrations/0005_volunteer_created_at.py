# Generated by Django 5.1.1 on 2024-10-02 17:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_successstory'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
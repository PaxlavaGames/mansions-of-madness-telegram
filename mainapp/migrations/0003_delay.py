# Generated by Django 5.2 on 2025-05-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_remove_drop_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True)),
                ('user_id', models.PositiveIntegerField()),
            ],
        ),
    ]

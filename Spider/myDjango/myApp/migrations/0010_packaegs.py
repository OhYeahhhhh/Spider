# Generated by Django 2.1.7 on 2019-04-24 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0009_auto_20190423_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packaegs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pPrice', models.CharField(max_length=7)),
                ('PTitle', models.CharField(max_length=100)),
            ],
        ),
    ]

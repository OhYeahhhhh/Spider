# Generated by Django 2.1.7 on 2019-04-13 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phones',
            name='pBrand',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='phones',
            name='pContent',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='phones',
            name='pNo',
            field=models.CharField(max_length=6),
        ),
    ]

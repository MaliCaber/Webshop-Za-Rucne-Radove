# Generated by Django 3.2.4 on 2022-12-17 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artikal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikal',
            name='kolicina_na_stanju',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

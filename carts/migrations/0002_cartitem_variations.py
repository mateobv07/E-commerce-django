# Generated by Django 3.2.6 on 2021-09-17 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_delete_variationmanager'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]

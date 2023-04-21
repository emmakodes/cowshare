# Generated by Django 4.1.7 on 2023-04-09 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_exchange_offer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref',
            field=models.CharField(default='ab', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='Nigeria', max_length=200),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-02 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='exclusions',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='message',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]

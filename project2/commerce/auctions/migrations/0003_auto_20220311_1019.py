# Generated by Django 3.2.9 on 2022-03-11 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bidding_category_comment_create_mywatchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create',
            name='DESCRIPTION',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='create',
            name='TITLE',
            field=models.CharField(max_length=30),
        ),
    ]

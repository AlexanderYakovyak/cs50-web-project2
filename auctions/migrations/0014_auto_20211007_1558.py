# Generated by Django 3.2.7 on 2021-10-07 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20211006_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='creator',
        ),
        migrations.AddField(
            model_name='user',
            name='listed_items',
            field=models.ManyToManyField(blank=True, related_name='creator', to='auctions.AuctionListing'),
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='auctions.AuctionListing'),
        ),
    ]

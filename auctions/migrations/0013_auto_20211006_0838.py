# Generated by Django 3.2.7 on 2021-10-06 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_rename_bids_numbers_auctionlisting_bids_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='category', to='auctions.AuctionListing'),
        ),
    ]

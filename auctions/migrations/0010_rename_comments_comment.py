# Generated by Django 3.2.7 on 2021-10-04 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auctionlisting_current_bid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
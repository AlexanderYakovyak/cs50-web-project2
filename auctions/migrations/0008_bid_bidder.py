# Generated by Django 3.2.7 on 2021-10-04 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20211004_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
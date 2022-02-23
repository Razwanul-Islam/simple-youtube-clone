# Generated by Django 3.1.4 on 2021-05-28 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='media/channel/profile/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='media/images/thumbnail/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='media/videos/'),
        ),
    ]
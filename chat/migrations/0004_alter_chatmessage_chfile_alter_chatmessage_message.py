# Generated by Django 4.1.7 on 2023-05-29 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatmessage_chfile_chatmessage_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='chfile',
            field=models.FileField(blank=True, null=True, upload_to='img/'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='message',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
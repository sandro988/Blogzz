# Generated by Django 4.1.6 on 2023-02-14 23:28

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_customuser_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_picture",
            field=imagekit.models.fields.ProcessedImageField(
                blank=True,
                default="profile_pictures/default_profile_picture.webp",
                upload_to="profile_pictures/users",
            ),
        ),
    ]

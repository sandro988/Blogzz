# Generated by Django 4.1.6 on 2023-04-09 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0006_comment_comment_downvotes_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="comment_downvotes_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="comment",
            name="comment_upvotes_count",
            field=models.IntegerField(default=0),
        ),
    ]

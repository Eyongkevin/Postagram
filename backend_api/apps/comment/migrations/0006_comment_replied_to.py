# Generated by Django 4.2.7 on 2023-11-22 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("apps_comment", "0005_remove_comment_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="replied_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_replied",
                to="apps_comment.comment",
            ),
        ),
    ]
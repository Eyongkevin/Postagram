# Generated by Django 4.2.7 on 2023-11-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apps_comment", "0006_comment_replied_to"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="comment",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("post__isnull", True),
                        ("replied_to__isnull", True),
                        _connector="OR",
                    ),
                    models.Q(
                        ("post__isnull", True),
                        ("replied_to__isnull", True),
                        _negated=True,
                    ),
                ),
                name="check_post_and_replied_to",
            ),
        ),
    ]

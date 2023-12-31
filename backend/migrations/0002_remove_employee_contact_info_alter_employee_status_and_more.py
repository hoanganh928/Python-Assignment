# Generated by Django 4.2.8 on 2023-12-21 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="employee", name="contact_info",),
        migrations.AlterField(
            model_name="employee",
            name="status",
            field=models.CharField(
                choices=[
                    ("ACTIVE", "ACTIVE"),
                    ("NOT_STARTED", "NOT_STARTED"),
                    ("TERMINATED", "TERMINATED"),
                ],
                db_index=True,
                max_length=50,
            ),
        ),
        migrations.CreateModel(
            name="ContactInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("phone", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend.employee",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]

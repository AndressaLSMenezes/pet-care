# Generated by Django 4.1.6 on 2023-02-13 02:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0003_pet_weight_alter_pet_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="sex",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Not Informed", "Not Informed"),
                ],
                default="Not Informed",
                max_length=20,
            ),
        ),
    ]
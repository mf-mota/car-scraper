# Generated by Django 5.0.1 on 2024-01-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_alter_car_mileage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='fuel',
            field=models.CharField(choices=[('benzyna', 'Benzyna'), ('benzyna+cng', 'Benzyna+CNG'), ('benzyna+lpg', 'Benzyna+LPG'), ('diesel', 'Diesel'), ('elektryczny', 'Elektryczny'), ('etanol', 'Etanol'), ('hybryda', 'Hybryda'), ('wodór', 'Wodór')], null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='gearbox',
            field=models.CharField(choices=[('automatyczna', 'Automatyczna'), ('manualna', 'Manualna')], null=True),
        ),
    ]
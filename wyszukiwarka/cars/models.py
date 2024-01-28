from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.id}/{self.name}"


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=40000, null=True)
    engine_size = models.IntegerField(null=True)
    bhp_count = models.IntegerField(null=True)
    mileage = models.IntegerField(null=True)

    FUEL_CHOICES = [("benzyna", "Benzyna"), 
                    ("benzyna+cng", "Benzyna+CNG"), 
                    ("benzyna+lpg", "Benzyna+LPG"),
                    ("diesel", "Diesel"), 
                    ("elektryczny", "Elektryczny"),
                    ("etanol", "Etanol"),
                    ("hybryda", "Hybryda"), 
                    ("wodór", "Wodór")]
    
    fuel = models.CharField(choices=FUEL_CHOICES, null=True)

    GEARBOX_CHOICES = [("automatyczna", "Automatyczna"), 
                       ("manualna", "Manualna")]
    gearbox = models.CharField(choices=GEARBOX_CHOICES, null=True)
    
    year = models.IntegerField()
    price = models.IntegerField()
    tk_lemmatized = models.TextField(max_length=40000, null=True)

    def __str__(self) -> str:
        return f"Car: {self.id}/{self.brand}/{self.title}"






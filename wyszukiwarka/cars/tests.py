from django.test import TestCase
from cars.models import Car, Brand
from cars import data_processer as dp

# Create your tests here.

class ModelTest(TestCase):
    def setUp(self):
        brand_1 = Brand.objects.create(
            name="TestBrand"
        )
        brand_2 = Brand.objects.create(
            name="TestBrand2"
        )
        car_1 = Car.objects.create(
            brand_id = brand_1.id,
            title="TestBrand Vehicle 2.0",
            summary="Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara",
            engine_size=1998,
            bhp_count=179,
            mileage=90570,
            fuel="diesel",
            gearbox="manualna",
            year=2016,
            price=78000,
            tk_lemmatized = dp.tokenize_lemmatize("Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara")
        )
        car_2 = Car.objects.create(
            brand_id = brand_1.id,
            title="TestBrand Vehicle 1.8 150",
            summary="Śliczny biały kolor. Dostępny od ręki. Od 1 właściciela",
            engine_size=1800,
            bhp_count=150,
            mileage=50000,
            fuel="benzyna",
            gearbox="manualna",
            year=2016,
            price=78000,
            tk_lemmatized = dp.tokenize_lemmatize("Śliczny biały kolor. Dostępny od ręki. 1 właściciel")
        )
        car_3 =  Car.objects.create(
            brand_id = brand_2.id,
            title="TestBrand2 Focus 1.6R2",
            summary="Focus 1.6, Nowe sprzęgło, rozrząd!!",
            engine_size=1599,
            bhp_count=170,
            mileage=350900,
            fuel="benzyna",
            gearbox="manualna",
            year=2009,
            price=30450,
            tk_lemmatized = dp.tokenize_lemmatize("Focus 1.6, Nowe sprzęgło, rozrząd!!")
        )

class BrandModelTest(ModelTest):
    def test_brand_model(self):
        brand = Brand.objects.all().filter(name="TestBrand2").first()
        self.assertEqual(brand.name, "TestBrand2", msg="Brand name mismatch")
        self.assertEqual(str(brand), f"{brand.id}/TestBrand2")

class CarModelTest(ModelTest):
    def test_car_model(self):
        car = Car.objects.all().filter(title="TestBrand Vehicle 1.8 150").first()
        self.assertEqual(car.title, "TestBrand Vehicle 1.8 150", msg="Title mismatch")
        self.assertEqual(car.brand.name, "TestBrand", msg="Brand mismatch") #brand
        self.assertEqual(car.summary, "Śliczny biały kolor. Dostępny od ręki. Od 1 właściciela", msg="Summary mismatch") #sumary
        self.assertEqual(car.engine_size, 1800, msg="Engine mismatch") #engine size
        self.assertEqual(car.bhp_count, 150, msg="BHP mismatch") #bhp count
        self.assertEqual(car.mileage, 50000, msg="Mileage mismatch") #mileage
        self.assertEqual(car.fuel, "benzyna", msg="Fuel mismatch") #fuel
        self.assertEqual(car.gearbox, "manualna", msg="Gearbox mismatch") #gearbox
        self.assertEqual(car.year, 2016, msg="Year mismatch") #year
        self.assertEqual(car.tk_lemmatized, dp.tokenize_lemmatize("Śliczny biały kolor. Dostępny od ręki. 1 właściciel"), 
                         msg="lemmatized summary mismatch") #tk
        self.assertEqual(str(car), f"Car: {car.id}/{car.brand}/{car.title}", msg="String representation mismatch")









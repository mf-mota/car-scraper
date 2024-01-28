from django.core.management.base import BaseCommand
from cars.models import Car, Brand
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException    
from django.db import connection
from wyszukiwarka.settings import DATABASES
from django.db import transaction
import cars.data_processer as dp
from wyszukiwarka import settings
from sqlalchemy import create_engine
import environ
env = environ.Env()
environ.Env.read_env()

db_def = DATABASES['default']


def search_otomoto(brand):
    '''Scrapes otomoto data and saves it in a pandas df'''

    def make_url(brand):
        url = f"https://www.otomoto.pl/osobowe/{brand}/?search%5Bfilter_enum_damaged%5D=0"
        return url


    def get_id_or_new_brand(brand_name):
        db_brand = Brand.objects.all().filter(name=brand_name).first()
        if db_brand:
            return db_brand.id
        else:
            new_brand = Brand.objects.create(name=brand_name)  
            print("new brand: ", new_brand)
            return new_brand.id 
        

    def extract_key_props(listing, selector, data_type=int):
        try:
            element = listing.find_element(By.CSS_SELECTOR, f"dd[data-parameter='{selector}']")
            data = data_type(element.text.replace(" ", "").replace("km", ""))
        except:
            data = None
        return data
    
    def extract_price(listing):
        try:
            price = int(listing.find_element(By.CSS_SELECTOR, "div div h3").text.replace(" ", ""))
        except:
            price = None
        return price

    def listings_to_df(brand_name):

        conn_str = f"{env('DB_TYPE')://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}}"
        engine_con = create_engine(conn_str).connect()
        browser = browser = webdriver.Chrome()
        brand_id = get_id_or_new_brand(brand_name=brand_name)
        
        def find_page_number(browser):
            try:
                time.sleep(2)
                browser.find_elements(By.CSS_SELECTOR, "li[data-testid='pagination-list-item']")[-1].find_element(By.CSS_SELECTOR, "a")
            except:
                return 1
            else: 
                return int(browser.find_elements(By.CSS_SELECTOR, "li[data-testid='pagination-list-item']")[-1].find_element(By.CSS_SELECTOR, "a").text)
        
        browser.get(make_url(brand_name))

        pages = find_page_number(browser=browser)
        print("pages: ", pages)
        columns = ['title', 'summary', 'engine_size', 'bhp_count', 'mileage', 'fuel', 'gearbox', 'year', 'price', 'brand_id']
        df = pd.DataFrame(columns=columns)

        for page_number in range(0, 10):
            time.sleep(0.5)
            listings = browser.find_elements(By.CSS_SELECTOR, "div[data-testid='search-results'] div > article[data-orientation='horizontal'] > section")

            for listing in listings:
                title = listing.find_element(By.CSS_SELECTOR, "div h1 a").text
                pojem_km_summary = listing.find_element(By.CSS_SELECTOR, "div h1 a").find_element(By.XPATH, "../..").find_element(By.CSS_SELECTOR, "p").text.split(" • ")
                pojemnosc, moc, summary = None, None, None

                for value in pojem_km_summary:
                    if "cm3" in value and len(value) < 10:
                        pojemnosc = int(value.replace(" cm3", "").replace(" ", ""))
                    elif "KM" in value and len(value) < 9:
                        moc = int(value.replace(" KM", ""))
                    else:
                        summary = value

                mileage = extract_key_props(listing=listing, selector="mileage")
                fuel = extract_key_props(listing=listing, selector="fuel_type", data_type=str)
                gearbox = extract_key_props(listing=listing, selector="gearbox", data_type=str)
                year = extract_key_props(listing=listing, selector="year")
                price = extract_price(listing=listing)

                df.loc[len(df)] = [title, summary, pojemnosc, moc, mileage, fuel, gearbox, year, price, brand_id]

            if page_number % 5 == 0:
                print(df)
                try:
                    df_ft = dp.process_df_summary(df)
                    print("ft: ", df_ft)
                    with transaction.atomic():
                        df_ft.to_sql('cars_car', con=engine_con, index=False, if_exists="append")
                        engine_con.commit()

                except Exception as e:
                    pass

                df = pd.DataFrame(columns=columns)
                df_ft = pd.DataFrame(columns=columns)
                time.sleep(0.1)
            if page_number < pages - 1:
                browser.get(make_url(brand)+"&page="+str(page_number+2))


        df_ft = dp.process_df_summary(df)
        df_ft.to_sql('cars_car', con=engine_con, index=False, if_exists="append")
        engine_con.commit()
        

    listings_to_df(brand)





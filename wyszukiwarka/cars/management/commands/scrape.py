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
from cars.scraper import search_otomoto


class Command(BaseCommand):
    help = "Scrape vehicles from otomoto and add them to the db"

    def add_arguments(self, parser):
        parser.add_argument("brand", type=str)
        
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Scraping started... \n'))
        try:
            search_otomoto(kwargs["brand"])
        except Exception as error:
            self.stderr.write(self.style.ERROR(f'\nError scraping otomoto... {error}'))
        else:
            self.stdout.write(self.style.SUCCESS('\nScraping complete!'))

        



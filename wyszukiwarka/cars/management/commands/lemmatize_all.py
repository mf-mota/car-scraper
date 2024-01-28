from django.core.management.base import BaseCommand
from cars.models import Car
import spacy
import pandas as pd
from django.db import transaction
from unidecode import unidecode


class Command(BaseCommand):
    help = 'Update tk_lemmatized field for existing Car records'

    @transaction.atomic
    def handle(self, *args, **options):
        spacy.prefer_gpu()
        nlp = spacy.load("pl_core_news_lg")

        def tokenize_lemmatize(text):
                if not text:
                    return None
                doc = nlp(text)
                lemmas = [unidecode(token.lemma_.lower()) for token in doc if not token.is_punct]
                return " ".join(lemmas)

        # Get all Car records
        cars = Car.objects.all()

        # Loop through each record and update tk_lemmatized
        for car in cars:
            car.tk_lemmatized = tokenize_lemmatize(car.summary)
            print(car.id)
            car.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated tk_lemmatized for all Car records'))
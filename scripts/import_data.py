from django.conf import settings

from restaurants.data import import_csv


def run():
    path = settings.BASE_DIR / 'restaurants' / 'restaurants.csv'
    import_csv(path)

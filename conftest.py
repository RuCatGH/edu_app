import pytest
from django.conf import settings


def pytest_configure():
    settings.DEBUG = False
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

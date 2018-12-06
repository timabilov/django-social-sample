from socialplatform.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['*']
# other production configurations..

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = ()

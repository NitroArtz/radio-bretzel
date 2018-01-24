import os

class Config(object):

    SITE_NAME = os.environ.get('SITE_NAME','Radio Bretzel Backend')

    DOCKER_URL = os.environ.get('DOCKER_URL', 'unix://var/run/docker.sock')
    DOCKER_VERSION = os.environ.get('DOCKER_VERSION', 'auto')

    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'database.radiobretzel')

class Dev(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False

class Test(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

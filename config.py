import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    USERNAME = 'admin',
    PASSWORD = 'default'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
               'sqlite:///' + os.path.join(base_dir,'app' , 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # disable signaling the app on every modification
    #app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    MAIL_SERVER = os.environ.get('MAIR_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['miso.arbutina@gmail.com']
    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'es']

    TESTING = False

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
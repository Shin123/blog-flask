import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 5


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')
    SECRET_KEY = '0\xbb5\x1f\xbe0\xfe\nS\xdaeO\x8c\xc6\xf6T.`/\xb9\xea\x0f*d'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # SQLALCHEMY_DATABASE_URI = (
    #     'postgresql://postgres:postgres@localhost:5432/mastering_flask'
    # )

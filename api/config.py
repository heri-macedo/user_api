class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_db.db'
    DEBUG = True

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True
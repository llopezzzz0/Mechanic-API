
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:ZeroGonYuki25!@localhost/mechanic_db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'SimpleCache'
    
    
class ProductionConfig:
    pass
    
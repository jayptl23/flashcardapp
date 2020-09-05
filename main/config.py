from dotenv import load_dotenv
import os

load_dotenv()


class Config():
    # Default environment is dev
    ENV = "production"
    if ENV == "dev":
        # TODO: set debug to true
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
    else:
        # TODO: set debug to false
        DEBUG = False
        SQLALCHEMY_DATABASE_URI = os.getenv('PROD_SQLALCHEMY_DATABASE_URI')

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    print(type(SECRET_KEY), SECRET_KEY)
    print(type(SQLALCHEMY_DATABASE_URI), SQLALCHEMY_DATABASE_URI)
    print(SQLALCHEMY_DATABASE_URI == "sqlite:///site.db")

import os
from dotenv import load_dotenv
import oracledb

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_TNS_NAME = os.getenv("DB_TNS_NAME")
    DB_WALLET_DIR = os.getenv("DB_WALLET_DIR")
    WALLET_PASSWORD = os.getenv("DB_WALLET_PASSWORD", "Carlostomi12*")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "config_dir": DB_WALLET_DIR,
            "wallet_location": DB_WALLET_DIR,
            "wallet_password": WALLET_PASSWORD
        }
    }

    # URI estándar solo como placeholder
    SQLALCHEMY_DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_TNS_NAME}"
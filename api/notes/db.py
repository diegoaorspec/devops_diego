from flask import current_app
from pymongo import MongoClient


def init_app(app):
    client = app.config.get("MONGO_CLIENT")
    if client is None:
        client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=2000)
    app.extensions["mongo"] = client


def get_client():
    return current_app.extensions["mongo"]


def get_db():
    return get_client().get_default_database()

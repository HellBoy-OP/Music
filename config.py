from os import environ


class Config(object):
    API_ID = environ.get("API_ID", 0)
    API_HASH = environ.get("API_HASH", None)
    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    DB_URI = environ.get("MONGO_URL", None)
    LOGGER_ID = environ.get("LOG_GROUP", 0)
    HEROKU_API = environ.get("HEROKU_API", None)
    HEROKU_APP = environ.get("HEROKU_APP", None)
    HELLBOT_SESSION = environ.get("HELLBOT_SESSION", None)
    TMP_DIR = environ.get("TMP_DIR", "./DOWNLOADS/")

    # Soon

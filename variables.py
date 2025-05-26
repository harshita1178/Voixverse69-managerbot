# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX


import json
import os


def get_user_list(config, key):
    with open("{}/Mikobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    # Configuration class for the bot

    # Enable or disable logging
    LOGGER = True

    # <================================================ REQUIRED ======================================================>
    # Telegram API configuration
    API_ID = 20952516 # Get this value from my.telegram.org/apps
    API_HASH = "4b7997216605cd4dd9cb2ee513838955"

    # Database configuration (PostgreSQL)
    DATABASE_URL = "postgresql://dbvoixverse_user:FS7FWzyHyts2wUgYqrn6b702Wqo4KahS@dpg-d0q286odl3ps73b8hbc0-a.oregon-postgres.render.com/dbvoixverse"

    # Event logs chat ID and message dump chat ID
    EVENT_LOGS = -1002617754650
    MESSAGE_DUMP = -1002331557980

    # MongoDB configuration
    MONGO_DB_URI = "mongodb+srv://VOIXVERSE1789:ANIMELOVER11@voixverse-managerbot.m11s3b8.mongodb.net/?retryWrites=true&w=majority&appName=Voixverse-managerbot"

    # Support chat and support ID
    SUPPORT_CHAT = "https://t.me/VoixVerse_Studioss"
    SUPPORT_ID = -1002668191611

    # Database name
    DB_NAME = "Voixverse-managerbot"

    # Bot token
    TOKEN = "7581829695:AAGCcqcbUBuyb8cpBpwpE9OBzxHaILWeNIA"  # Get bot token from @BotFather on Telegram

    # Owner's Telegram user ID (Must be an integer)
    OWNER_ID = 6675050163
    # <=======================================================================================================>

    # <================================================ OPTIONAL ======================================================>
    # Optional configuration fields

    # List of groups to blacklist
    BL_CHATS = []

    # User IDs of sudo users, dev users, support users, tiger users, and whitelist users
    DRAGONS = get_user_list("elevated_users.json", "sudos")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    DEMONS = get_user_list("elevated_users.json", "supports")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    # Toggle features
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    # Modules to load or exclude
    LOAD = []
    NO_LOAD = []

    # Global ban settings
    STRICT_GBAN = True
    BAN_STICKER = (
        "CAACAgUAAxkBAAEGWC5lloYv1tiI3-KPguoH5YX-RveWugACoQ4AAi4b2FQGdUhawbi91DQE"
    )

    # Temporary download directory
    TEMP_DOWNLOAD_DIRECTORY = "./"
    # <=======================================================================================================>


# <=======================================================================================================>


class Production(Config):
    # Production configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True


class Development(Config):
    # Development configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True

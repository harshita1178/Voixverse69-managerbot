from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from Mikobot import DB_URI
from Mikobot import LOGGER as log

if DB_URI and DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://", 1)


# ENGINE, BASE aur SESSION ko global scope mein define kiya gaya hai
# taki doosri files inhe import kar saken
ENGINE = None # Pehle None assign kiya gaya hai
BASE = declarative_base() # BASE ko yahan define kar rahe hain
SESSION = None # SESSION ko bhi pehle None assign kiya gaya hai


def start() -> scoped_session:
    global ENGINE, SESSION # Global variables ko modify karne ke liye declare kiya
    
    log.info("[PostgreSQL] Connecting to database......")
    
    # ENGINE ko DB_URI se initialize kiya ja raha hai
    ENGINE = create_engine(DB_URI, client_encoding="utf8")
    
    # BASE ke metadata ko ENGINE se bind kiya gaya hai
    BASE.metadata.bind = ENGINE
    
    # Tables create karte waqt ENGINE ko bind kiya gaya hai
    # Yeh change Table.create() missing bind argument error ko fix karega
    BASE.metadata.create_all(bind=ENGINE)
    
    # Session factory banaya gaya hai aur SESSION ko initialize kiya gaya hai
    SESSION = scoped_session(sessionmaker(bind=ENGINE, autoflush=False))
    
    return SESSION # Ab start() function SESSION return karega


try:
    SESSION = start() # start() function ko call karke SESSION ko initialize kiya ja raha hai
except Exception as e:
    log.exception(f"[PostgreSQL] Failed to connect due to {e}")
    exit()

log.info("[PostgreSQL] Connection successful, session started.")

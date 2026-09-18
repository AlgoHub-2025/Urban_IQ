import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Centralized Configuration
class Config:
    AQICN_TOKEN = os.getenv("AQICN_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reports.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Configure Global Logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("UrbanIQ")

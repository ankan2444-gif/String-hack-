import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID", "36522229")
API_HASH = os.getenv("API_HASH", "7f27443617af60bcb0e23f7147d3eaf9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "9214074207:AAG7cCyOnfh8HA72lur7ijC8wCPY9cA-R0Y")
SUDOERS = list(map(int, os.getenv("SUDOERS", "7723735360").split()))
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://alexfahad303_db_user:5fKktFkH8ZhFkLTF@cluster0.60mt60g.mongodb.net/?appName=Cluster0")
LOG_GROUP_ID = os.getenv("LOG_GROUP_ID", "-1004381576208")
MUST_JOIN = os.getenv("MUST_JOIN", "LYNX_MADARA")
DISABLED = os.getenv("DISABLED", "").split()

if not API_ID:
    raise SystemExit("No API_ID found. Exiting...")
elif not API_HASH:
    raise SystemExit("No API_HASH found. Exiting...")
elif not BOT_TOKEN:
    raise SystemExit("No BOT_TOKEN found. Exiting...")

if not MONGO_URL:
    print("MONGO_URL environment variable Is Empty Bot")

# Convert the LOG_GROUP_ID variable to an integer if it is not None
if LOG_GROUP_ID:
    LOG_GROUP_ID = int(LOG_GROUP_ID)

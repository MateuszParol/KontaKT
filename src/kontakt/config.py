
import os
from platformdirs import user_data_dir

APP_NAME = "KontaKT"
APP_AUTHOR = "MateuszParol"

# Resolve user data directory (e.g., AppData/Local/MateuszParol/KontaKT)
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)

# Database path
DB_FILE = os.path.join(USER_DATA_DIR, "kontakt.db")

# Ensure directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)

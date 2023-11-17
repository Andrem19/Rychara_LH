import threading
from models.settings import Settings

time_format = "%Y-%m-%d %H:%M:%S"
settings_gl: Settings = Settings()
global_var_lock = threading.Lock()
coins_in_work = {}
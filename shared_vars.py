import threading
from models.settings import Settings

settings_gl: Settings = Settings()
global_var_lock = threading.Lock()
coins_in_work = {}
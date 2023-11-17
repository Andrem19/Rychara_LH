import json

class Settings:
    def __init__(self):
        self.exchange: str = 'KC'
        self.name: str = ''
        self.API_KEY: str = 'KCAPI_1'
        self.SECRET_KEY: str = 'KCSECRET_1'
        self.telegram_token: str = ''
        self.coin: str = 'BTCUSDT'
        self.message_timer: int = 15
        self.target_len: int = 5
        self.amount_usdt: float = 20
        self.init_stop_loss: float = 0.008
        self.distance: float = 0.001
        self.border_saldo: str = '03.09.23'

    def to_json(self):
            with open(f"settings/settings_UNIVERSAL.json", "w") as file:
                json.dump(self.__dict__, file)
        
    def from_json(self):
        with open(f"settings/settings_UNIVERSAL.json", "r") as file:
            data = json.load(file)
            for key, value in data.items():
                setattr(self, key, value)

set = Settings()
set.to_json()
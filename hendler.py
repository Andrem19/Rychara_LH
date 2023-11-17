import json
from datetime import datetime
import shared_vars as sv
from exchange_workers.bybit_http import BybitAPI
from exchange_workers.kucoin import KuCoin
import helpers.firebase as fb
import exchange_workers.exchanges as ex
import work
import threading
import asyncio
import copy


def handler(signals: str) -> None:

    sign_dic = json.loads(signals)

    timestamp = sign_dic['timestamp']
    name = sign_dic['name']
    
    if name == sv.settings_gl.name and (timestamp+30 > datetime.now().timestamp() or timestamp == 111):
        print(f'{signals}')
        coin_symbol = sign_dic['coin']
        signal = sign_dic[coin_symbol]
        if signal != 3:
            is_position_exist, position = ex.is_position_exist(ex.get_position_info(coin_symbol))
            if is_position_exist == False and coin_symbol not in sv.coins_in_work:
                settings = None
                ent = None
                with sv.global_var_lock:
                    sv.coins_in_work[coin_symbol] = signal
                    ent = json.dumps(sv.coins_in_work)
                    settings = copy.deepcopy(sv.settings_gl)
                fb.write_data('status', 'entitys', sv.settings_gl.name, ent)
                settings.coin = coin_symbol
                close_thread = threading.Thread(target=asyncio.run, args=(work.open_position(settings, signal),))
                close_thread.start()

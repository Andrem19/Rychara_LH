import shared_vars as sv
from models.settings import Settings
import helpers.firebase as fb
from exchange_workers.bybit_http import BybitAPI
from exchange_workers.kucoin import KuCoin
import hendler as hn
import time
import sys

def on_signal_change(doc_snapshot, changes, read_time):
    for change in changes:
        if change.document.id == sv.settings_gl.name:
            new_value = change.document.to_dict().get('signal')
            if new_value is not None:
                hn.handler(new_value)

def main(args=None):
    if args is None:
        args = [1]
    sv.settings_gl = Settings()
    sv.settings_gl.from_json()
    argument1 = int(args[0])
    sv.settings_gl.name = f'ent_{argument1}'
    sv.settings_gl.exchange = args[1]
    sv.settings_gl.telegram_token = f'API_TOKEN_{argument1}'
    sv.settings_gl.API_KEY = f'{sv.settings_gl.exchange}API_{argument1}'
    sv.settings_gl.SECRET_KEY = f'{sv.settings_gl.exchange}SECRET_{argument1}'
    if sv.settings_gl.exchange == 'BB':
        BybitAPI.init(sv.settings_gl)
    elif sv.settings_gl.exchange == 'KC':
        KuCoin.init(sv.settings_gl)
    print(f'Settings load successfuly with arguments: {args}')

    doc_ref = fb.db.collection('signal').document(sv.settings_gl.name)
    doc_ref.on_snapshot(on_signal_change)


if __name__ == '__main__':
    main(sys.argv[1:])
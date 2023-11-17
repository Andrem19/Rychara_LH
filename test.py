import exchange_workers.exchanges as ex
from exchange_workers.kucoin import KuCoin
import shared_vars as sv
#pasphrase passphrase

KuCoin.init(sv.settings_gl)

is_pos_exist, position = ex.is_position_exist(ex.get_position_info('AVAXUSDT'))

print(is_pos_exist)

print('---------------------------------')

print(position)
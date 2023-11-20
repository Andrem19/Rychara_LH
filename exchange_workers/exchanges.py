from models.settings import Settings
from exchange_workers.bybit_http import BybitAPI
from exchange_workers.kucoin import KuCoin
from models.position import Position
import helpers.telegr as tel
import shared_vars as sv
import datetime
import asyncio
import time

def cancel_order(order_id):
    if sv.settings_gl.exchange == 'BB':
        pass
    elif sv.settings_gl.exchange == 'KC':
        KuCoin.cancel_order_byId(order_id)

def trailing_SL(position: Position, price: float) -> str:
    sd = 'Buy' if position.signal == 1 else 'Sell'
    if sv.settings_gl.exchange == 'BB':
        pass
    elif sv.settings_gl.exchange == 'KC':
        return KuCoin.trailing_SL(position.coin, sd, position.amount, price)

def close_time_finish(position: Position):
    sd = 'Buy' if position.signal == 1 else 'Sell'
    if sv.settings_gl.exchange =='BB':
        pass
    elif sv.settings_gl.exchange == 'KC':
        KuCoin.close_position_market(position.coin, sd, position.amount)

def get_last_price(coin: str):
    if sv.settings_gl.exchange == 'BB':
        return BybitAPI.get_last_price(coin)
    elif sv.settings_gl.exchange == 'KC':
        return KuCoin.get_last_price(coin)

def get_balance():
    balance = 0
    if sv.settings_gl.exchange == 'BB':
        balance = BybitAPI.get_balance('USDT')
    elif sv.settings_gl.exchange == 'KC':
        balance = KuCoin.get_balance('USDT')
    return float(balance)


def is_position_exist(position: str):
    if sv.settings_gl.exchange == 'BB':
        if float(position['size']) == 0:
            return False, position
    elif sv.settings_gl.exchange == 'KC':
        if float(position['currentQty']) == 0:
            return False, position
    elif sv.settings_gl.exchange == 'BN':
        pass
    return True, position

def get_position_info(coin: str):
    position = None
    if sv.settings_gl.exchange == 'BB':
        position = BybitAPI.get_position_info(coin)
    elif sv.settings_gl.exchange == 'KC':
        position = KuCoin.get_position(coin)
    elif sv.settings_gl.exchange == 'BN':
        pass
    return position

# 1 - buy 2 - sell
async def place_order(settings: Settings, buy_sell: int):
    bs = 'Buy' if buy_sell == 1 else 'Sell'
    order_id = ''
    timest = datetime.datetime.now().timestamp()
    if settings.exchange == 'BB':
        print(settings.coin)
        print(bs)
        print(settings.amount_usdt)
        response = BybitAPI.place_order(False, settings.coin, bs, settings.amount_usdt, 0.0001, TP_perc=None, SL_perc=None)
        
        if 'retMsg' in response and response['retMsg'] == 'OK':
            order_id = response['result']['orderId']
            open_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('retMsg = OK')
            while True:
                
                resp = BybitAPI.get_position_info(settings.coin)
                if float(resp['size']) > 0:
                    old_balance = BybitAPI.get_balance('USDT')
                    current_position = Position(settings.coin, open_time , float(resp['avgPrice']), old_balance, float(resp['size']), buy_sell)

                    await tel.send_inform_message(settings.telegram_token, f'Position was taken successfully: {str(current_position)}', '', False)
                    return True, current_position
                
                time.sleep(1)
                
                time_obj = datetime.datetime.strptime(open_time, sv.time_format)
                duration = datetime.datetime.now() - time_obj
                duration_seconds = duration.total_seconds()

                if timest + settings.message_timer < datetime.datetime.now().timestamp():
                    print(f'trying to take position {duration}')
                    await tel.send_inform_message(settings.telegram_token, f'Trying to take position {duration}', '', False)
                    timest = datetime.datetime.now().timestamp()
                
                if duration_seconds > 60:
                    break
            
            BybitAPI.cancel_orders(settings.coin, order_id)
            await tel.send_inform_message(settings.telegram_token, 'Position doesn\'t exist after order', '', False)
            return False, None
        
        else:
            print('some problem to place order')
    
    elif settings.exchange == 'KC':
        print(settings.coin)
        print(bs)
        print(settings.amount_usdt)
        order_id = KuCoin.open_limit_order(settings.coin, bs, settings.amount_usdt)
        if 'orderId' in order_id:
            open_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('order placed')
            while True:
                is_pos_exist, position = is_position_exist(get_position_info(settings.coin))
                if is_pos_exist == True:
                    old_balance = get_balance()
                    current_position = Position(settings.coin, open_time , float(position['avgEntryPrice']), old_balance, float(position['currentQty']), buy_sell)

                    await tel.send_inform_message(settings.telegram_token, f'Position was taken successfully: {str(current_position)}', '', False)
                    current_position.order_sl_id = KuCoin.open_SL(settings.coin, bs, current_position.amount, current_position.price_open, settings.init_stop_loss)
                    return True, current_position
                
                time.sleep(1)
                time_format = "%Y-%m-%d %H:%M:%S"
                time_obj = datetime.datetime.strptime(open_time, time_format)
                duration = datetime.datetime.now() - time_obj
                duration_seconds = duration.total_seconds()

                if timest + settings.message_timer < datetime.datetime.now().timestamp():
                    print(f'trying to take position {duration}')
                    await tel.send_inform_message(settings.telegram_token, f'Trying to take position {duration}', '', False)
                    timest = datetime.datetime.now().timestamp()
                
                if duration_seconds > 60:
                    break
            
            KuCoin.cancel_order_byId(order_id['orderId'])
            await tel.send_inform_message(settings.telegram_token, 'Position doesn\'t exist after order', '', False)
            return False, None
        
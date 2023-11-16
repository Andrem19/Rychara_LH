from models.settings import Settings
from exchange_workers.bybit_http import BybitAPI
from models.position import Position
import helpers.telegr as tel
import datetime
import asyncio
import time

# 1 - buy 2 - sell
async def place_order(settings: Settings, buy_sell: int):
    bs = 'Buy' if buy_sell == 1 else 'Sell'
    order_id = ''
    timest = datetime.datetime.now().timestamp()
    if settings.exchange == 'BB':
        print(settings.coin)
        print(bs)
        print(settings.amount_usdt)
        response = BybitAPI.place_order(False, settings.coin, bs, settings.amount_usdt, settings.order_in_perc, TP_perc=None, SL_perc=None)
        
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
            
            BybitAPI.cancel_orders(settings.coin, order_id)
            await tel.send_inform_message(settings.telegram_token, 'Position doesn\'t exist after order', '', False)
            return False, None
        
        else:
            print('some problem to place order')
    
    elif settings.exchange == 'KC':
        pass
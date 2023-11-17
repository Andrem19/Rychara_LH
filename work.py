from models.settings import Settings
from models.position import Position
import exchange_workers.exchanges as ex
from exchange_workers.bybit_http import BybitAPI
import json
import helpers.firebase as fb
import helpers.telegr as tel
import helpers.services as ser
import helpers.firebase as fb
import datetime
import shared_vars as sv
import time


async def open_position(settings: Settings, signal: int):
    try:
        close_order = False
        print('start open position')
        time_start = datetime.datetime.now().timestamp()
        res, cur_pos = await ex.place_order(settings, signal)
        last_border_sl = cur_pos.price_open
        if not res:
            position_wasnt_open(settings)
        while res:
            time.sleep(2)
            last_price = ex.get_last_price(settings.coin)
            time_obj = datetime.datetime.strptime(cur_pos.time_open, sv.time_format)
            duration = datetime.datetime.now() - time_obj
            duration_seconds = duration.total_seconds()
            cur_pos.duration = duration_seconds
            res, responce = ex.is_position_exist(ex.get_position_info(settings.coin))
            if duration_seconds >= settings.target_len * 1 * 60 and not close_order:
                print('time to close')
                ex.close_time_finish(cur_pos)
                close_order = True
            
            if not close_order:
                if last_price > last_border_sl * (1+settings.distance*2) and signal == 1:
                    stop_loss = (1 + settings.distance) * last_border_sl
                    if last_price > last_border_sl * (1+settings.distance*4):
                        stop_loss = (1 + settings.distance*2) * last_border_sl
                    ex.trailing_SL(cur_pos, stop_loss)
                    last_border_sl = stop_loss
                elif last_price < last_border_sl * (1-settings.distance*2) and signal == 2:
                    stop_loss = (1 - settings.distance) * last_border_sl
                    if last_price < last_border_sl * (1-settings.distance*4):
                        stop_loss = (1 - settings.distance*2) * last_border_sl
                    ex.trailing_SL(cur_pos, stop_loss)
                    last_border_sl = stop_loss
            
            if time_start + settings.message_timer < datetime.datetime.now().timestamp():
                await handle_message(settings, responce, duration)
                time_start = datetime.datetime.now().timestamp()
                
        await handle_position()

    except Exception as e:
        print(f'Error: {e}')
        await tel.send_inform_message(settings.telegram_token, f'Error: {e}', '', False)
                
async def handle_message(settings: Settings, response, duration):
    message = f'coin: {settings.coin}\nunrealisedPnl: {response["unrealisedPnl"]}\nduration: {duration}'
    print(message)
    await tel.send_inform_message(settings.telegram_token, message, '', None)

async def position_wasnt_open(settings: Settings):
    message = f'Position wasn\'t open'
    print(message)
    await tel.send_inform_message(settings.telegram_token, message, '', None)
    with sv.global_var_lock:
        sv.coins_in_work.pop(settings.coin)
        ent = json.dumps(sv.coins_in_work)
        fb.write_data('status', 'entitys', sv.settings_gl.name, ent)

async def handle_position():
    pass


                
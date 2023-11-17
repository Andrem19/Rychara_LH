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
    print('start open position')
    time_start = datetime.datetime.now().timestamp()
    res, cur_pos = await ex.place_order(settings, signal)
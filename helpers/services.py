import json
import os
import shared_vars as sv
from datetime import datetime
from models.position import Position
from models.settings import Settings

def get_unrealized_PNL(responce: dict):
    if sv.settings_gl.exchange == 'BB':
        return float(responce['unrealisedPnl'])
    elif sv.settings_gl.exchange == 'KC':
        return float(responce['unrealisedPnl'])


def convert_to_timestamp(date_string):
    if date_string == '0':
        return 0
    try:
        dt = datetime.strptime(date_string, '%d.%m.%y')
        timestamp = dt.timestamp() * 1000
        return int(timestamp)
    except ValueError:
        return -1

def filter_list_by_timestamp(input_list, timestamp):
    if timestamp == 0:
        return input_list
    filtered_list = []
    for item in input_list:
        if item[0] >= timestamp:
            filtered_list.append(item)
    return filtered_list

def convert_seconds_to_period(seconds: float):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = round(seconds % 60, 2)

    period = f"{hours:02}:{minutes:02}:{seconds:02}"
    return period

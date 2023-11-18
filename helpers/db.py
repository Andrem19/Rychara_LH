import json
import os
from models.position import Position

def add_pos_to_db(item: Position, path):
    with open(path, 'a') as file:
        json.dump(item.__dict__, file)
        file.write('\n')

def add_saldo(item: list, path: str):
    with open(path, 'a') as file:
        item[1] = round(item[1], 3)
        file.write(f'{item[0]},{item[1]}' + "\n")

def get_last_saldo():
    path = '_db/saldo.txt'
    data = []
    if os.path.isfile(path):
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line != '':
                    parts = line.strip().split(',')
                    timestamp = float(parts[0])
                    value = float(parts[1])
                    data.append([timestamp, value])
        return data[-1][1]
    else:
        return 0


def read_deser_positions(coin: str) -> list[Position]:
    positions = []
    file_path = f'positions/position_{coin}.json'

    # Check if file exists
    print('read deser pos')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                position = Position(data['coin'], data['time_open'], data['price_open'], data['old_balance'], data['amount'], data['signal'])
                position.new_balance = data['new_balance']
                position.profit = data['profit']
                position.price_close = data['price_close'] if data['price_close'] else 0
                position.duration = data['duration']
                position.time_close = data['time_close'] if data['time_close'] else None
                positions.append(position)

    return positions
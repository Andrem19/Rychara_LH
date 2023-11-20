from kucoin_futures.client import Trade
from kucoin_futures.client import Market
from kucoin_futures.client import User
from models.settings import Settings
from decouple import config
import threading

round_coins = {
    'ALGOUSDT': 4,
    'DOTUSDT': 3,
    'FILUSDT': 3,
    'GALAUSDT': 5,
    'XRPUSDT': 4,
    'VETUSDT': 5,
    'MATICUSDT': 4,
    'FTMUSDT': 4,
    'KAVAUSDT': 4,
    'MANAUSDT': 4,
    'ATOMUSDT': 3,
    'ADAUSDT': 5,
    'FLOWUSDT': 4,
    'AXSUSDT': 3,
    'SOLUSDT': 3,
    'INJUSDT': 3,
    'EGLDUSDT': 2,
    'GRTUSDT': 5,
    'DOGEUSDT': 5,
    'SNXUSDT': 3,
    'APTUSDT': 3,
    'NEOUSDT': 3,
    'SUIUSDT': 4,
    'MINAUSDT': 4,
    'RNDRUSDT': 4,
    'XMRUSDT': 2,
    'TRXUSDT': 5,
    'UNIUSDT': 3,
    'LTCUSDT': 2,
    'AAVEUSDT': 2,
    'XLMUSDT': 5,
    'AVAXUSDT': 2,
    'STXUSDT': 4,
    'SANDUSDT': 5,
    'THETAUSDT': 4,
    'APEUSDT': 3,
    'DYDXUSDT': 3,
}

amount_lot = {
    'ALGOUSDT': 1,
    'DOTUSDT': 1,
    'FILUSDT': 0.01,
    'GALAUSDT': 1,
    'XRPUSDT': 10,
    'VETUSDT': 100,
    'MATICUSDT': 10,
    'FTMUSDT': 1,
    'KAVAUSDT': 0.1,
    'MANAUSDT': 1,
    'ATOMUSDT': 1,
    'ADAUSDT': 10,
    'FLOWUSDT': 0.1,
    'AXSUSDT': 0.1,
    'SOLUSDT': 0.1,
    'INJUSDT': 1,
    'EGLDUSDT': 0.01,
    'GRTUSDT': 1,
    'DOGEUSDT': 100,
    'SNXUSDT': 0.1,
    'APTUSDT': 0.1,
    'NEOUSDT': 0.1,
    'SUIUSDT': 1,
    'MINAUSDT': 1,
    'RNDRUSDT': 1,
    'XMRUSDT': 0.01,
    'TRXUSDT': 100,
    'UNIUSDT': 1,
    'LTCUSDT': 0.1,
    'AAVEUSDT': 0.01,
    'XLMUSDT': 10,
    'AVAXUSDT': 0.1,
    'STXUSDT': 1,
    'SANDUSDT': 1,
    'THETAUSDT': 0.1,
    'APEUSDT': 0.1,
    'DYDXUSDT': 0.1,
}

class KuCoin:
    @staticmethod
    def open_limit_order(coin: str, sd: str, amount_usdt: int) -> str:
        curent_price = KuCoin.get_last_price(coin)
        lot = (amount_usdt / curent_price) // amount_lot[coin]
        side = 'buy' if sd == 'Buy' else 'sell'
        pr = 0
        if side == 'buy':
            pr = curent_price * (1+0.0001)
        else:
            pr = curent_price * (1-0.0001)
        order_id = KuCoin.client.create_limit_order(symbol=f'{coin}M', side=side, lever='5', size=int(lot), price=round(pr, round_coins[coin]))
        return order_id
    
    @staticmethod
    def cancel_order_byId(order_id: str) -> str:
        try:
            result = KuCoin.client.cancel_order(orderId=order_id)
            print(result)
        except Exception as e:
            print(f'Error: {e}')

    @staticmethod
    def close_position_market(coin: str, sd: str, amount_lot: str) -> str:
        side = 'buy' if sd == 'Buy' else 'sell'
        order_id = KuCoin.client.create_market_order(symbol=f'{coin}M', side=side, lever='5', size=amount_lot, closeOrder=True)
        return order_id
    
    @staticmethod
    def get_position(coin: str):
        position = KuCoin.client.get_position_details(f'{coin}M') # 'unrealisedPnl' 'currentQty'/0
        return position
    
    @staticmethod
    def open_SL(coin: str, sd: str, amount_lot: str, open_price: float, SL_perc: float) -> str:
        side = 'buy' if sd == 'Sell' else 'sell'
        st = 'down' if side =='sell' else 'up'
        price = 0
        if side == 'buy':
            price = open_price * (1+SL_perc)
        elif side == 'sell':
            price = open_price * (1-SL_perc)

        order_id = KuCoin.client.create_limit_order(symbol=f'{coin}M', side=side, size=amount_lot, lever='5', closeOrder=True, stopPriceType='IP', price=round(price, round_coins[coin]), stopPrice=round(price, round_coins[coin]), stop=st)
        return order_id['orderId']
    
    @staticmethod
    def trailing_SL(coin: str, sd: str, amount_lot: str, price: float) -> str:
        side = 'buy' if sd == 'Sell' else 'sell'
        st = 'down' if side =='sell' else 'up'

        order_id = KuCoin.client.create_limit_order(symbol=f'{coin}M', side=side, size=amount_lot, lever='5', closeOrder=True, stopPriceType='IP', price=round(price, round_coins[coin]), stopPrice=round(price, round_coins[coin]), stop=st)
        return order_id['orderId']
    

    @staticmethod
    def open_TP(coin: str, sd: str, amount_lot: str, open_price: float, TP_perc: float) -> str:
        side = 'buy' if sd == 'Sell' else 'sell'
        st = 'up' if side =='sell' else 'down'
        price = 0
        if side == 'buy':
            price = open_price * (1-TP_perc)
        elif side == 'sell':
            price = open_price * (1+TP_perc)
        
        order_id = KuCoin.client.create_limit_order(symbol=f'{coin}M', side=side, size=amount_lot, lever='5', closeOrder=True, stopPriceType='TP', price=round(price, round_coins[coin]), stopPrice=round(price, round_coins[coin]), stop=st)
        return order_id
    
    @staticmethod
    def get_last_price(coin):
        tk = KuCoin.market_client.get_ticker(f'{coin}M')
        curent_price = float(tk['price'])
        return curent_price
         
    @staticmethod
    def get_balance(coin: str):
        result = KuCoin.user_client.get_account_overview(currency=coin) # 'availableBalance' 'accountEquity'
        return result['accountEquity']
    
    


    client: Trade = None
    market_client: Market = None
    user_client: User = None
    init_lock = threading.Lock() 

    @staticmethod
    def init(settings: Settings):
        # Check if the variables are already set
        if KuCoin.client is not None:
                return
        
        # Acquire the lock to ensure only one thread initializes the variables
        with KuCoin.init_lock:
            # Check again after acquiring the lock in case another thread has already initialized the variables
            if KuCoin.client is not None:
                return
            
            # Set the variables from shared_vars module
            KuCoin.user_client = User(key=config(settings.API_KEY), secret=config(settings.SECRET_KEY), passphrase='passphrase', is_sandbox=False, url='https://api-futures.kucoin.com')
            KuCoin.market_client = Market(url='https://api-futures.kucoin.com')
            KuCoin.client = Trade(key=config(settings.API_KEY), secret=config(settings.SECRET_KEY), passphrase='passphrase', is_sandbox=False, url='https://api-futures.kucoin.com')
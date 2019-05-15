import typing as _t
import requests
import random
# import _thread
import threading
import time


_ID_COUNTER = 1
_CURRENCY_USED_TO_BY = 'PLN'
_CURRENCY_BEING_SOLD = 'BTC'

_SERVICE_BTC_ONE = 'https://bitbay.net/API/Public/BTCPLN/ticker.json'
_SERVICE_BTC_TWO = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTCPLN?fbclid=IwAR0_XnPm2aRV2KpmifWQklAabfZDE-x-km1MV2qqny-NYf34z7K6xtSq2K0'


def compare_exchange():
    try:
        _btc_one = requests.get(_SERVICE_BTC_ONE).json()
        _btc_two = requests.get(_SERVICE_BTC_TWO).json()

        ask_one, bid_one = float(_btc_one['ask']), float(_btc_one['bid'])
        ask_two, bid_two = float(_btc_two['ask']), float(_btc_two['bid'])

        ret_ask = 0
        if ask_one > ask_two:
            print(f"Bardziej opłaca się pierwszy ask_one: {ask_one}, ask_two: {ask_two}")
        else:
            print(f"Bardziej opłaca się drugi ask_one: {ask_one}, ask_two: {ask_two}")

        if bid_one > bid_two:
            print(f"Bardziej opłaca się pierwszy bid_one: {bid_one}, bid_two: {bid_two}")
        else:
            print(f"Bardziej opłaca się drugi bid_one: {bid_one}, bid_two: {bid_two}")
    except Exception as err:
        pass


class User:
    __slots__ = ['id', 'gender', 'first_name', 'last_name', 'login', 'email', 'assets']

    def __init__(self, id: int, login: str, email: str, gender: str, firstname: str = '', lastname: str = '', assets = None):
        super().__init__()
        if not id:
            raise ValueError('id required')
        self.id = id
        if not login:
            raise ValueError('login required')
        self.login = login
        if not email:
            raise ValueError('email required')
        self.email = email
        if not gender:
            raise ValueError('gender required')
        self.gender = gender

        self.first_name = firstname
        self.last_name = lastname
        self.assets = assets

    @property
    def name(self):
        return '{0} {1}'.format(self.first_name.capitalize(), self.last_name.capitalize())

    @property
    def btc(self) -> float:
        if not self.assets:
            return 0
        else:
            return self.assets.get('BTC', 0)

    @btc.setter
    def btc(self, value: float):
        if not self.assets:
            self.assets = {}
        self.assets['BTC'] = value

    @property
    def pln(self) -> float:
        if not self.assets:
            return 0
        else:
            return self.assets.get('PLN', 0)

    @pln.setter
    def pln(self, value: float):
        if not self.assets:
            self.assets = {}
        self.assets['PLN'] = value

    def __str__(self) -> str:
        return '%s [id: %d, login: %s, assets: %s]' % (self.name, self.id, self.login, str(self.assets))


class Transaction:
    __slots__ = ['seller', 'buyer', 'amount_bought', 'amount_payed']

    def __init__(self, seller: User, buyer: User, amount_bought: float, amount_payed: float):
        super().__init__()
        self.seller = seller
        self.buyer = buyer
        self.amount_bought = amount_bought
        self.amount_payed = amount_payed

    def __str__(self):
        return '{0} bought {1} {bought_currency} for {2} {used_currency} from {3}'.format(self.buyer, self.amount_bought, self.amount_payed, self.seller, bought_currency=_CURRENCY_BEING_SOLD, used_currency=_CURRENCY_USED_TO_BY)


def get_random_users(count: int) -> _t.List[User]:
    response = requests.get('https://randomuser.me/api/?results=%d' % (count,))
    if response.status_code != 200:
        raise ConnectionError('unexpected status code: %d' % (response.status_code,))
    users_json = (response.json())['results']
    ret_users = []
    global _ID_COUNTER
    for uj in users_json:
        uj_id = _ID_COUNTER
        _ID_COUNTER += 1
        assets = {'BTC': random.random() * 3, 'PLN': random.randint(1000, 100000)}
        u = User(uj_id, uj['login']['username'], uj['email'], uj['gender'], uj['name']['first'], uj['name']['last'], assets)
        ret_users.append(u)
    return ret_users


def join_users_in_pairs(users: _t.List[User]):
    if len(users) % 2 != 0:
        raise ValueError('users list must have odd amount of elements')
    users_shuffled = users.copy()
    random.shuffle(users_shuffled)
    split_inx = len(users) // 2
    half = users_shuffled[:split_inx]
    other_half = users_shuffled[split_inx:]
    return list(zip(half, other_half))


def simulate_transaction(user_pairs: _t.List[_t.Tuple[User, User]], exchange: dict, ret_transactions: list):
    users_copy = user_pairs.copy()
    while users_copy:
        involved_users = users_copy.pop()
        buyer = involved_users[1]
        seller = involved_users[0]
        buy_exchange = exchange['buy']
        seller_btc_owned = seller.btc
        full_sale_cost = seller_btc_owned * buy_exchange
        if full_sale_cost > buyer.pln:
            fraction = buyer.pln / buy_exchange
            bought_amount = fraction * seller_btc_owned
            seller.btc -= bought_amount
            money_spent = buyer.pln
            buyer.pln = 0.0
        else:
            bought_amount = seller.btc
            seller.btc = 0
            money_spent = full_sale_cost
            buyer.pln -= money_spent
        transaction = Transaction(seller, buyer, bought_amount, money_spent)
        ret_transactions.append(transaction)
        print(transaction)
        if random.random() < .5:
            time.sleep(.25)


if __name__ == '__main__':
    compare_exchange()

    users = get_random_users(100)
    users_joined = join_users_in_pairs(users)

    ret_transactions = []
    exchange_rate = {'buy': 22297.34, 'sell': 22272.34}
    simulation = threading.Thread(target=simulate_transaction, args=[users_joined, exchange_rate, ret_transactions])

    print('Running simulation...')
    simulation.start()
    simulation.join()


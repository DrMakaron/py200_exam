from hashlib import md5
from string import ascii_letters, digits
from random import randint


GUITARS_DATABASE = [
    {'name': 'Gibson Les Paul Paul Landers Signature',
     'price': 1000.00,
     'rating': 10.00},
    {'name': 'ESP E-II RZK-I BURNT',
     'price': 2000.00,
     'rating': 10.00},
    {'name': 'ESP SNAKEBYTE Black Satin',
     'price': 2000.00,
     'rating': 9.55},
    {'name': 'ESP LTD KH-WZ',
     'price': 500.00,
     'rating': -100.00}
]

class IdCounter:

    _counter = 0

    @property
    def counter(self):
        return self._counter

    def counter_up(self):
        def inner():
            self._counter += 1
            return self._counter

        return inner


class Password:
    def __init__(self, password):
        if not isinstance(password, str):
            raise TypeError

        if len(password) < 8:
            raise ValueError

        if any(char not in ascii_letters + digits for char in password):
            raise ValueError

        self.password = password


    def check_password(self, hash_password):
        return md5(self.password.encode()) == hash_password

    def get_password(self):
        return md5(self.password.encode())


class Product:
    def __init__(self, name, price, rating):

        self._id = randint(1, 1000000)

        if not isinstance(name, str):
            raise TypeError

        self._check_price(price)
        self._check_rating(rating)

        self._name = name
        self._price = price
        self._rating = rating

    def __str__(self):
        return f'{self._id}: {self._name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name!r}, price={self.price!r}, rating={self.rating!r})'

    @staticmethod
    def _check_price(price):
        if not isinstance(price, float):
            raise TypeError
        if price < 0:
            raise ValueError

    @staticmethod
    def _check_rating(rating):
        if not isinstance(rating, float):
            raise TypeError
        if not -100.0 <= rating <= 100.0:
            raise ValueError

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        self._check_price(value)
        self._price = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._check_rating(value)
        self._rating = value


class Cart:

    products = []

    @classmethod
    def add_product(cls, product):
        cls.products.append(product)

    @classmethod
    def remove_product(cls, product):
        cls.products.remove(product)

    @classmethod
    def show(cls):
        return cls.products

class User:

    _PASSWORD_PLUG = 'password1'

    def __init__(self, username, password, cart):
        self._id = randint(1, 1000000)

        if not isinstance(username, str):
            raise TypeError

        self._username = username
        self.__password = Password(password).get_password()
        self._cart = cart

    @property
    def cart(self):
        return self._cart

    @property
    def username(self):
        return self._username

    def __str__(self):
        return f'Username: {self._username}, cart: {self._cart.show()}'

    def __repr__(self):
        return f'{self.__class__.__name__}(username={self._username!r}, password={self._PASSWORD_PLUG}!r)'


class Store:

    user = None

    def define_user(self, user):
        self.user = user

    @staticmethod
    def add_to_cart(products):
        product = products[randint(0, len(products) - 1)]
        Cart.add_product(product)
        return Cart


if __name__ == '__main__':
    products_list = [
        Product(name=guitar['name'], price=guitar['price'], rating=guitar['rating']) for guitar in GUITARS_DATABASE
    ]

    name = input('Enter username: ')
    pass_ = input('Enter password: ')

    store = Store()
    cart = store.add_to_cart(products_list)
    user_ = User(name, pass_, cart)
    print(user_)

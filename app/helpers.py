from app.models import User, Coins

def usd(value):
    """Formats value as USD."""
    return "${:,.2f}".format(value)

def number(value):
    """Formats value as comma seperated number."""
    return "{:,.2f}".format(value)

def wholenumber(value):
    """Formats value as comma seperated whole number."""
    return "{:,.0f}".format(value)

def percent(value):
    """Formats value as percent."""
    return "{:,.2f}%".format(value)

def totalcoin(userid, short):
    coinid = Coins.query.filter_by(short=short).first().id
    coins = User.query.get(userid).transaction.filter_by(coins_id=coinid).all()
    coinsnumber = 0.0
    for coin in coins:
        coinsnumber += coin.number
    print("helpers.py Totalcoin: {}".format(coinsnumber))
    return coinsnumber

def timefilter(value):
    return str(value)[:-4]

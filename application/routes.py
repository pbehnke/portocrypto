import requests
from application import application, db
from application.helpers import *
from application.forms import LoginForm, RegistrationForm, TransForm, ChangeForm
from flask_login import current_user, login_user,  login_required, logout_user
from application.models import User, Transactions, Coins
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from passlib.apps import custom_app_context as pwd_context


application.jinja_env.filters["usd"] = usd
application.jinja_env.filters["percent"] = percent
application.jinja_env.filters["number"] = number
application.jinja_env.filters["time"] = timefilter
application.jinja_env.filters["wnumber"] = wholenumber

@application.route("/")
@application.route('/index')
def index():

    #importing information on all coins for frontpage
    url = "http://coincap.io/front"
    frontcoins = requests.get(url)
    frontcoins = frontcoins.json()
    # session.user_id=0


    # create Forms for index
    logform = LoginForm()
    regform = RegistrationForm()
    transform = TransForm()
    changeform = ChangeForm()

    if current_user.is_active:

        # getting users cash Amount
        cash = current_user.cash

        # getting users transactions
        trans = current_user.transaction.all()

        url = "http://coincap.io/page/{}"

        gtotal = cash

        for t in trans:
            t.short = Coins.query.get(t.coins_id).short

            coininfo = requests.get(url.format(t.short)).json()

            t.longname =  Coins.query.get(t.coins_id).longname
            t.newprice = coininfo['price']
            t.newtotal = t.newprice * t.number
            gtotal += t.newtotal
            t.pricediff = t.newprice - t.price
            t.totaldiff = (t.newprice * t.number) - (t.price * t.number)
            t.allcoin = totalcoin(current_user.id, t.short)

        return render_template('index.html', frontcoins = frontcoins, title='Sign In', logform=logform, regform=regform, gtotaldiff = 10000, transform=transform, trans=trans, gtotal=gtotal, cash=cash, coins=trans, changeform=changeform)

    return render_template('index.html', frontcoins = frontcoins, title='Sign In', logform=logform, regform=regform, transform=transform, changeform=changeform)

@application.route("/transaction", methods=['POST'])
@login_required
def transaction():
    """Buy or sell coins."""

    transform = TransForm()

    print("HERE: {}".format(transform.buyOrsell.data))

    if transform.validate_on_submit():
        coin = Coins.query.filter_by(short=transform.short.data).first()
        if coin is None:
            addcoin = Coins(short=transform.short.data, longname=transform.longname.data)
            db.session.add(addcoin)
            db.session.commit()
            # print("added Coin")
        # recognizing if buy or sell, if sell make number negative
        if transform.buyOrsell.data == True:
            transform.number.data = -transform.number.data
        coin = Coins.query.filter_by(short=transform.short.data).first()
        transaction = Transactions(user_id=current_user.id, coins_id=coin.id, number=transform.number.data, price=transform.price.data)
        # updating users cash amount
        User.query.get(current_user.id).cash -= (transform.number.data * transform.price.data)
        db.session.add(transaction)
        db.session.commit()

        return jsonify(status='ok')
    flash('Error Error')
    return jsonify(transform.errors)

@application.route("/login", methods=['POST'])
def login():
    """Log user in."""

    logform = LoginForm()

    if logform.validate_on_submit():
        user = User.query.filter_by(username=logform.username.data).first()
        if user is None or not user.check_password(logform.password.data):
            return jsonify("User doesn't exist or Password wrong")
        login_user(user, remember=logform.remember_me.data)
        return jsonify(status='ok')
    return jsonify("Error")

@application.route("/logout")
@login_required
def logout():
    """Log user out."""

    logout_user()
    return redirect(url_for('index'))

@application.route("/register", methods=["POST"])
def register():
    """Register user."""

    regform = RegistrationForm()

    if regform.validate_on_submit():
        user = User(username=regform.username.data, email=regform.email.data)
        user.set_password(regform.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify(status='ok')
    return jsonify(regform.errors)

@application.route("/password", methods=["POST"])
@login_required
def password():
    """Change password."""

    changeform = ChangeForm()

    if changeform.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        if changeform.oldPassword.data == changeform.newPassword.data:
            return jsonify("Old and New Password can not match")
        if user is None or not user.check_password(changeform.oldPassword.data):
            return jsonify("Old Password wrong")
        user.set_password(changeform.newPassword.data)
        db.session.commit()
        return jsonify(status='ok')
    return jsonify("Error")

@application.route("/check", methods=['POST'])
def check():

    data = {}

    short = request.form['short']
    price = request.form['price']

    try:
        Coins.query.filter_by(short=short).first()
        coinid = Coins.query.filter_by(short=short).first().id
        coins = User.query.get(current_user.id).transaction.filter_by(coins_id=coinid).all()
        coinsnumber = 0.0
        for coin in coins:
            coinsnumber += coin.number

        data['coinsnumber'] = coinsnumber
    except:
        data['coinsnumber'] = 0

    cash = User.query.get(current_user.id).cash

    amount = cash / float(price)

    data['amount'] = amount
    data['cash'] = cash

    return jsonify(data)

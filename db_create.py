from application import db
from application.models import User, Transactions, Coins

db.create_all()

print("DB created.")

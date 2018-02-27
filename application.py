import os
from application import application, db
from application.models import User, Transactions, Coins

# adding database instance and models to the shell session
@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transactions': Transactions, 'Coins': Coins}

if __name__ == "__main__":
    application.debug = True
    application.run()

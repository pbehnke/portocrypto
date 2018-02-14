import os
from app import app, db
from app.models import User, Transactions, Coins

# adding database instance and models to the shell session
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transactions': Transactions, 'Coins': Coins}

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

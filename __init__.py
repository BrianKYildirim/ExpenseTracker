from flask import Flask
from models.database import Database
from route import routes
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'expense_tracker.db')

db = Database(app.config['DATABASE'])
db.initialize_db()

app.register_blueprint(routes.bp)

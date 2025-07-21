from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from .db import connection
from .mikoshi import bp as mikoshi_bp
from .auth_bp import bp as auth_bp
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
load_dotenv()

#LLamado de variables de entorno
app.config['DB_HOST'] = os.getenv('DB_HOST')
app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['DB'] = os.getenv('DB')
connection.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(mikoshi_bp)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
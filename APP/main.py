from flask import Flask, render_template
from dotenv import load_dotenv
import os


load_dotenv()
flask_app= os.getenv('FLASK_APP')
flask_dev= os.getenv('FLASK_DEBUG')


app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'key',
    DB_HOST= os.environ.get('FLASK_DB_HOST'),
    DB_USER= os.environ.get('FLASK_DB_USERT'),
    DB_PASSWORD= os.environ.get('FLASK_DB_PASSWORD'),
    DB= os.environ.get('FLASK')
)

@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.html')

@app.route('/Sobre MI', methods=['GET'])
def Sobre_Mi():
    return render_template('sobre_me.html')

if __name__ == '__main__':
    app(debug=True)



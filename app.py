from flask import Flask

from app_config import config

app = Flask(__name__)

if __name__ =='__main__':
    app.run(debug=config['DEBUG'], host=config['HOST'], port=config['HOST'])
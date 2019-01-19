from flask import Flask

from db import db
from app_config import config
from resources.blog_posts import blog_posts_api

# TODO install --> marshmallow, flask-marshmallow, marshmallow-sqlalchamey, flask-sqlalchemy

app = Flask(__name__)
app.secret_key = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True



app.register_blueprint(blog_posts_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return 'Testing'


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=config['DEBUG'], host=config['HOST'], port=config['PORT'])

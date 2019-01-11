from flask import Flask

from app_config import config
from resources.blog_posts import blog_posts_api


app = Flask(__name__)
app.register_blueprint(blog_posts_api, url_prefix='/api/v1')

@app.route('/')
def index():
    return 'Testing'

if __name__ == '__main__':
    app.run(debug=config['DEBUG'], host=config['HOST'], port=config['PORT'])

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from .config import Config
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
api = Api(app)

# migrate = Migrate(app, db)

def create_tables():
    with app.app_context():
        db.create_all()

# Initialize Flasgger with Flask app
Swagger(app, template_file='./static/swagger.yaml')

from .resources import UserResource, ChildResource, BlogResource, HomeFeedResource

api.add_resource(UserResource, '/user', '/user/<int:user_id>')
api.add_resource(ChildResource, '/child', '/child/<int:child_id>')
api.add_resource(BlogResource, '/blog', '/blog/<int:blog_id>')
api.add_resource(HomeFeedResource, '/homefeed/<int:user_id>')

@app.route('/')
def home():
    return "Server is running!"

if __name__ == '__main__':
    app.run(debug=True)
    create_tables()

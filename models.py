"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Bagel_with_sesame_3.jpg/800px-Bagel_with_sesame_3.jpg'

db = SQLAlchemy()

def connect_db(app):
    """Connect to the database"""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    posts = db.relationship('Post', backref='user')

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    first_name = db.Column(
        db.String(25),
        nullable = False
    )

    last_name = db.Column(
        db.String(25),
        nullable = False
    )

    image_url = db.Column(
        db.String,
        nullable = False,
        default = DEFAULT_IMAGE_URL
    )

class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(
        db.Integer,
        primary_key = True
    )

    title = db.Column(
        db.String(50),
        nullable = False
    )

    content = db.Column(
        db.String,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        nullable = False,
        default = db.func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )


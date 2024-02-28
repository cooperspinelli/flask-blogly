"""Blogly application."""

import os

from flask import Flask, render_template
from models import connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretsecret"

connect_db(app)

@app.get('/users')
def list_users():
    """List users with an add button."""

    users = User.query.all()
    return render_template("users.html", users=users)


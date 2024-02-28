"""Blogly application."""

import os

from flask import Flask, render_template, redirect, request
from models import connect_db, User, db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretsecret"

connect_db(app)


@app.get('/')
def redirect_to_users():
    """Redirects to users page"""

    return redirect('/users')

@app.get('/users')
def list_users():
    """List users with an add button."""

    users = User.query.all()
    return render_template("users.html", users=users)


@app.get('/users/new')
def new_user_form():
    """Returns form to create new user"""

    return render_template('new_user.html')


@app.post('/users/new')
def create_new_user():
    """Creates a new user record and redirects to the users list."""

    first = request.form['first']
    last = request.form['last']
    url = request.form['image_url']

    new_user = User(first_name = first,
                    last_name = last,
                    image_url = url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def display_user_details(user_id):
    """Displays user page."""
    user = User.query.get_or_404(user_id)

    return render_template('user_details.html', user=user)


@app.get('/users/<int:user_id>/edit')
def display_edit_page(user_id):
    """Displays page that allows user to edit their information."""

    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)
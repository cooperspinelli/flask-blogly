"""Blogly application."""

import os

from flask import Flask, render_template, redirect, request
from models import connect_db, User, Post, db
# from flask_debugtoolbar import DebugToolbarExtension

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

    # method chain an order by on that bad boi
    users = User.query.all()
    return render_template("users.html", users=users)


@app.get('/users/new')
def new_user_form():
    """Returns form to create new user"""

    return render_template('new_user.html')


@app.post('/users/new')
def create_new_user():
    """Creates a new user record and redirects to the users list."""

    new_user = User(first_name=request.form['first'],
                    last_name=request.form['last'],
                    image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()
    # flash some positive feedback

    return redirect('/users')


@app.get('/users/<int:user_id>')
def display_user_details(user_id):
    """Displays user page."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template('user_details.html', user=user, posts=posts)


@app.get('/users/<int:user_id>/edit')
def display_edit_page(user_id):
    """Displays page that allows user to edit their information."""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edits users information based on form input and
    redirects to users page"""

    # get or 404
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image_url']
    # do some extra checking here TODO:

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes user based on id and redirects to users page"""

    # get or 404
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    # flash a message

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def display_new_post_form(user_id):
    """Displays form for users to make a new post."""

    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def new_post(user_id):

    new_post = Post(title = request.form['title'],
                    content = request.form['content'],
                    user_id = user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Displays post details"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id):
    """Displays form that allows users to edit a post."""

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)

@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edits post data and redirects back to the post."""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')

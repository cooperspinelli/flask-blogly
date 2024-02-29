import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        # Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_users(self):
        """Tests user list display"""

        with app.test_client() as c:
            resp = c.get("/users")

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)

            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_user_details_display(self):
        """Tests page for displaying user details"""

        with app.test_client() as c:
            resp = c.get(f'/users/{self.user_id}')

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(f'<form action="/users/{self.user_id}/edit', html)
            self.assertIn(f'<form action="/users/{self.user_id}/delete', html)


    def test_new_user(self):
        """Tests creation of new user"""

        with app.test_client() as c:
            resp = c.post(
                '/users/new',
                data={'first': 'David',
                      'last': 'Sapiro',
                      'image_url': ''}
                )

            self.assertEqual(resp.status_code, 302)

            user_david = User.query.filter_by(first_name = 'David').one()
            self.assertEqual(user_david.image_url, DEFAULT_IMAGE_URL)


    def test_edit_form_display(self):
        """Tests edit form display"""

        with app.test_client() as c:
            resp = c.get(f'/users/{self.user_id}/edit')

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn('<h1>Edit A User</h1>', html)
            self.assertIn(f'<form action="/users/{self.user_id}" method="GET">', html)


    def test_edit_user(self):
        """Tests editing of a user"""

        with app.test_client() as c:
            resp = c.post(
                f'/users/{self.user_id}/edit',
                data={'first': 'New',
                      'last': 'Name',
                      'image_url': DEFAULT_IMAGE_URL}
                )

            self.assertEqual(resp.status_code, 302)

            edited_user = User.query.filter_by(first_name = 'New').one()
            self.assertEqual(edited_user.last_name, 'Name')

    def test_new_post(self):
        """Tests creating new post"""

        with app.test_client() as c:
            resp = c.post(
                f'/users/{self.user_id}/posts/new',
                data={'title': 'Test Post',
                      'content': 'This post is a test post'},
                follow_redirects = True)

            self.assertEqual(resp.status_code, 200)

            post_id = Post.query.filter_by(title='Test Post').one().post_id
            html = resp.get_data(as_text=True)
            self.assertIn(f'<li><a href="/posts/{post_id}"> Test Post </a></li>', html)


from models import db, Post, Tag

def delete_post_from_db(post_id):
    """Takes in post id and deletes post from database"""

    post = Post.query.get(post_id)
    post.tags = []
    db.session.delete(post)
    db.session.commit()

def delete_tag_from_db(tag_id):

    tag = Tag.query.get(tag_id)
    tag.posts = []
    db.session.delete(tag)
    db.session.commit()
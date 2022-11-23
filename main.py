import datetime

from flask import Flask, render_template
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username=''):
        self.username = username

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title=''):
        self.title = title

    def __repr__(self):
        return f'<Post {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title=''):
        self.title = title

    def __repr__(self):
        return f'<Tag {self.title}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment {self.text[:15]}>'


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = (
        db.session.query(Tag, func.count(tags.c.post_id).label('total'))
        .join(tags)
        .group_by(Tag)
        .order_by(desc('total'))
        .limit(5)
        .all()
    )

    return recent, top_tags


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page=page, per_page=app.config.get('POSTS_PER_PAGE', 10), error_out=False
    )
    recent, top_tags = sidebar_data()
    return render_template('home.html', posts=posts, recent=recent, top_tags=top_tags)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
    )


@app.route('/posts_by_tag/<string:tag_name>')
def posts_by_tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html', tag=tag, posts=posts, recent=recent, top_tags=top_tags
    )


@app.route('/posts_by_user/<string:username>')
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html', user=user, posts=posts, recent=recent, top_tags=top_tags
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
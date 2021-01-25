from app import db
from flask_login import UserMixin


        

    

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    username =  db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    contato = db.Column(db.String(60))
    flag = db.Column(db.String(30))
    languages = db.relationship('Languages', backref='author', lazy=True)
    posts = db.relationship('Posts', backref='author', lazy=True)
   


class Response(db.Model):
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name =  db.Column(db.String(30))
    content = db.Column(db.Text)
    comments_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE', onupdate='CASCADE'))

class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name =  db.Column(db.String(30), unique=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',  ondelete='CASCADE', onupdate='CASCADE'))
    relation = db.relationship(Response, backref="comments", passive_deletes=True, passive_updates=True)


class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    title = db.Column(db.String(20))
    subtitle = db.Column(db.String(30))
    text = db.Column(db.Text)
    key = db.Column(db.String(20))
    exercise = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    languageKey = db.Column(db.String(20), db.ForeignKey('languages.key', ondelete='CASCADE', onupdate='CASCADE'))
    relation = db.relationship(Comments, backref="posts", passive_deletes=True, passive_updates=True)

class Languages(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))
    image = db.Column(db.String(40))
    key = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    relation = db.relationship(Posts, backref="languages", passive_deletes=True, passive_updates=True)

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


 


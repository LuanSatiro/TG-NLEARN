from app import db



        
class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    subtitle = db.Column(db.String(30))
    text = db.Column(db.Text)
    key = db.Column(db.String(20))
    exercise = db.Column(db.Text)
    languageKey = db.Column(db.String(20), db.ForeignKey('languages.key', ondelete='CASCADE', onupdate='CASCADE'))
    

    def __init__(self, title, subtitle, text, key, exercise, languageKey):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.exercise = exercise
        self.key = key
        self.languageKey=languageKey

        

class Languages(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))
    image = db.Column(db.String(40))
    key = db.Column(db.String(20), unique=True)
    relation = db.relationship(Posts, backref="languages", passive_deletes=True, passive_updates=True)
    
    def __init__(self, title, description, image, key):
        self.title = title
        self.description = description
        self.image = image
        self.key = key    



class UserAdm(db.Model):
    __tablename__ = "useradm"

    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(30))
    password = db.Column(db.String(30))

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


    def __init__(self, username, password):
        self.username= username
        self.password = password



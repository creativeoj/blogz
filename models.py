from app import db, datetime, make_pw_hash

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)

    def __init__(self, title, content, owner, date=None):
        self.title = title
        self.content = content
        self.owner= owner
        if date is None:
            date = datetime.utcnow()
        self.date = date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash= db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):

        self.username = username
        self.pw_hash = make_pw_hash(password)


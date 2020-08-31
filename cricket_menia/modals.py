from cricket_menia import db

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    vill = db.Column(db.String(100))


    def __repr__(self):
        return '<User %r>' %self.name

def add_user(name, vill):
    new_user = users(name = name, vill = vill)
    db.session.add(new_user)
    db.session.commit()

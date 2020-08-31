from cricket_menia import db
from flask import session

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    vill = db.Column(db.String(100))


    def __repr__(self):
        return '<User %r>' %self.name

def already_loggedIn():
    if 'user_id' in session:
        return True
    else:
        return False

def user_info(user_id):
    return users.query.filter_by(_id = session['user_id']).first()

def is_authenticated(name, vill):
    guest = users.query.filter_by(name = name).first()
    if guest:
        if guest.vill == vill:
            return {'result': True, 'user': guest}
        else:        
            return {'result':False, 'msg':"Incorrect Village"}
    else:
        return {'result':False, 'msg':"User not found please SignUp"}



def add_user(name, vill):
    new_user = users(name = name, vill = vill)
    db.session.add(new_user)
    db.session.commit()

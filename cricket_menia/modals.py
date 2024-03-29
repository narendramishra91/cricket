from cricket_menia import db
from flask import session

class users(db.Model):
    """ table has the user detail"""

    _id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    vill = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' %self.name

class Following(db.Model):
    """ table has the detail of followers """

    _id = db.Column('id', db.Integer, primary_key = True)
    following = db.Column('following', db.Integer, db.ForeignKey('users.id'), nullable = False)
    follower = db.Column('follower', db.Integer, db.ForeignKey('users.id'), nullable = False)


def already_loggedIn():
    """ Cheaks if the user is logged in """

    if 'user_id' in session:
        return True
    else:
        return False
        

def user_info(user_id):
    """ Returs the user info for given id """

    response = users.query.filter_by(_id = session['user_id']).first()
    return response

def is_authenticated(name, vill):
    """ Cheaks if user's authentication """

    guest = users.query.filter_by(name = name).first()
    if guest:
        if guest.vill == vill:
            response = {'result': True, 'user': guest}
            return response
        else:
            response =  {'result':False, 'msg':"Incorrect Village"}     
            return response
    else:
        response = {'result':False, 'msg':"User not found please SignUp"}
        return response



def add_user(name, vill):
    """ Adds the user to the database """
    new_user = users(name = name, vill = vill)
    db.session.add(new_user)
    db.session.commit()

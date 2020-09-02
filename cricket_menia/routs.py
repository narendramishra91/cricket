from flask import render_template, request, url_for, flash, session, redirect, jsonify
from cricket_menia.modals import users, add_user, already_loggedIn, user_info, is_authenticated, add_relation, get_data_Following
from cricket_menia.modals import following_already
from cricket_menia import app


@app.route('/')
def home():
    """ This route goes to the home page"""

    # if user is loggedIn
    if already_loggedIn():
        return render_template('home.html', user_info = user_info(session['user_id']) , all_users = users.query.all())
    # otherwise
    else:
        return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """ Cheaks if user is alredy looged in? if not then log the user in """

    # if user already logged in
    if already_loggedIn():
        return render_template('home.html', user_info = user_info(session['user_id']) , all_users = users.query.all())

    # if not loggedIn
    else:
        # if request is via Post Method
        if request.method == 'POST':
            guest_name = request.form['user_name']
            guest_vill = request.form['village']

            #cheak if user is authenticated
            authenticated = is_authenticated(guest_name, guest_vill)
            
            #if authenticated
            if authenticated['result']:
                session['user_id'] = authenticated['user']._id
                return render_template('home.html', user_info = user_info(session['user_id']), all_users = users.query.all())
            
            #if village is incorrect
            elif authenticated['msg'] == "Incorrect Village":
                flash(authenticated['msg'], 'danger')
                return render_template('login_page.html')
            
            #if user not in database
            else:
                error = 'Sorry! you are not registered'
                flash(error, 'info')
                return render_template('login_page.html')

        # if get request
        else: 
            return render_template('login_page.html')


@app.route('/logout')
def logout():
    """ Logs user out"""

    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/profile/<int:id>')
def profile(id):
    """ Returns the profile of user given id """

    # list of ids following
    following_ids = [user.following for user in get_data_Following(session["user_id"]) ]

    #list of the names of the following people
    following =[user_info(id) for id in following_ids]
    if session["user_id"] == id:
        return render_template('profile.html', user_info = user_info(id), same_user = True, following = following )
    else:
        return render_template('profile.html', user_info = user_info(id), 
        same_user = False, id = id, following_already = following_already(session['user_id'], id))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """ Register user """

    if request.method == 'POST':
        name = request.form['user_name']
        vill = request.form['village']
        add_user(name, vill)
        flash('registered sucessesfully', 'info')
        return redirect(url_for('login'))

    else:
        return render_template('register.html')

@app.route('/follow', methods =['POST'])
def follow():
    """
    this route will allow user to follow
    User1: current User, User2: to whome he is following
    """
    user1 = int(request.form['user1'])
    user2 = int(request.form['user2'])
    if not following_already(user1, user2):
        add_relation(user1, user2)
    return jsonify(status='success')
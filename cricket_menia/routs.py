from flask import render_template, request, url_for, flash, session, redirect
from cricket_menia.modals import users, add_user, already_loggedIn, user_info, is_authenticated
from cricket_menia import app


@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # if user already logged in
    if already_loggedIn():
        user_info = user_info()
        return render_template('home.html', user_info = user_info , all_users = users.query.all())

    # if not loggedIn
    else:
        # if request is via Post Method
        if request.method == 'POST':
            guest_name = request.form['user_name']
            guest_vill = request.form['village']

            #cheak if user is authenticated
            authenticated = is_authenticated(guest_name, guest_vill)
            
            #if authenticated
            if authenticated:
                return render_template('home.html', user_info = authenticated.user, all_users = users.query.all())
            
            #if village is incorrect
            elif authenticated.msg == "Incorrect Village":
                flash(authenticated.msg, 'danger')
                return render_template('login_page.html')
            
            #if user not in database
            else:
                error = 'Sorry! you are not registered'
                flash(error, 'info')
                return render_template('register.html')

        # if get request
        else: 
            return render_template('login_page.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/profile/<int:id>')
def profile(id):
    user_info = users.query.filter_by(_id = id).first()
    return render_template('profile.html', user_info = user_info)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['user_name']
        vill = request.form['village']
        add_user(name, vill)
        flash('registered sucessesfully', 'info')
        return redirect(url_for('login'))

    else:
        return render_template('register.html')



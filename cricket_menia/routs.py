from flask import render_template, request, url_for, flash, session, redirect
from cricket_menia.modals import users, add_user
from cricket_menia import app


@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    if 'user_id' in session:
        user_info = users.query.filter_by(_id = session['user_id']).first()
        return render_template('home.html', user_info = user_info, all_users = users.query.all())

    else:
        if request.method == 'POST':
            guest_name = request.form['user_name']
            guest = users.query.filter_by(name = guest_name).first()
            if guest:
                if guest.vill == request.form['village']:
                    session['user_id'] = guest._id
                    user_info = guest
                    return render_template('home.html', user_info = user_info, all_users = users.query.all())
                else:
                    error = 'Sorry! you have entered your village wrong'
                    flash(error, 'danger')
                    return render_template('login_page.html')
            else:
                error = 'Sorry! you are not registered'
                flash(error, 'info')
                return render_template('login_page.html')

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



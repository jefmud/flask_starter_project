import sys

# server parameters
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

# basic flask imports
from flask import (abort, Flask, flash, g, get_flashed_messages, redirect, render_template, request, url_for)

# adding flask_admin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.peewee import ModelView

# flask bootstrap
from flask_bootstrap import Bootstrap

# adding flask_login 
from flask_login import (LoginManager, UserMixin, login_user, login_required,
                         logout_user, current_user)

import forms
import models

app = Flask(__name__)
app.secret_key = 'PutYourSecretInHere'
Bootstrap(app)

# flask-admin setup
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        try:
            if current_user.is_admin:
                return render_template('admin.html')
        except Exception as e:
            print(e)
            pass # silently fail for unauthorized trying to access admin space
        
        return redirect(url_for('index'))
        
admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminView())
admin.add_view(ModelView(models.User))

# flask-login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """returns user user based on user_id or None"""
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

# request handlers
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

# Regular routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """show login screen, handle data"""
    if current_user.is_authenticated:
        flash('Please logout first.')
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = models.User.get(models.User.username==username)
            if user.authenticate(password):
                login_user(user)
                flash('Welcome {}'.format(user), category='success')
                return redirect(url_for('index'))
        except Exception as e:
            print(e)

        flash('Incorrect login information', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """logout the user"""
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Please logout before registering a new email', category='warning')
        return redirect(url_for('index'))

    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(email=form.email.data, password=form.password.data)
        except:
            flash("Problems registering this user = {}".format(form.email.data),
                  category='danger')
        else:
            flash("You have been registered as {}".format(form.email.data))
            return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/_user_audit')
@login_required
def _user_audit():
    if current_user.is_admin:
        models.audit_users()
        flash("User audit completed",category="success")
        return redirect(url_for('admin.index'))
    abort(403) # they should not have run this give 'em the 403
    
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    if '--createsuperuser' in sys.argv:
        models.create_superuser()
        print "** superuser created **"
    elif '--initdatabase' in sys.argv:
        models.initialize_database()
        print "** database initialized **"
    elif '--runserver' in sys.argv:
        # see settings at the top of the file
        app.run(host=HOST, port=PORT, debug=DEBUG)
    else:
        print "app.py valid command line options"
        print " --createsuperuser (allows creation of an administrative user)"
        print "--initdatabase (initializes the database if required)"
        print "--runserver (runs the server on port configured in source code)"

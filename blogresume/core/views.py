# core/views.py
from flask import render_template, redirect, request, Blueprint, url_for
from flask_login import login_user
from blogresume.models import User, BlogPost
from blogresume.users.forms import RegistrationForm, LoginForm
from blogresume import db

core = Blueprint('core', __name__)


@core.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    
    #built-in registration on homepage
    form = RegistrationForm()
    loginForm = LoginForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    elif loginForm.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('index.html', blog_posts=blog_posts, form=form, loginForm=loginForm)


@core.route('/info')
def info():
    return render_template('info.html')
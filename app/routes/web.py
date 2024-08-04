from flask import render_template
from flask_login import login_required
import sqlalchemy as sa

from app import app, db
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Kathmandu!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Deadpool and Wolverine Movie was so cool.'
        }
    ]

    return render_template('index.html', title='Home', posts=posts)


@app.route('/user/<username>')
@login_required
def user_show(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Beautiful day in Kathmandu!'},
        {'author': user, 'body': 'The Deadpool and Wolverine Movie was so cool.'},
        {'author': user, 'body': 'The New Avengers movie was so cool.'},
        {'author': user, 'body': 'The Avengers movie was so cool.'},
    ]

    return render_template('user.html', title='User', user=user, posts=posts)

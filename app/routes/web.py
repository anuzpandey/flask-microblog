from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
import sqlalchemy as sa

from app import app, db
from app.forms import EditProfileForm
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


@app.route('/user/<username>/profile')
@login_required
def user_profile_show(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Beautiful day in Kathmandu!'},
        {'author': user, 'body': 'The Deadpool and Wolverine Movie was so cool.'},
        {'author': user, 'body': 'The New Avengers movie was so cool.'},
        {'author': user, 'body': 'The Avengers movie was so cool.'},
    ]

    return render_template('user.html', title='User', user=user, posts=posts)


@app.route('/user/<username>/profile/edit', methods=['GET', 'POST'])
@login_required
def user_profile_edit(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Profile updated successfully.')

        return redirect(url_for('user_profile_edit', username=current_user.username))

    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.gender.data = current_user.gender

    return render_template('edit_user.html', title='Edit Profile', form=form)


from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
import pymysql
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
from functools import wraps
import uuid
import sq


def follow(user_id):
    c = sq.connection.cursor()
    check = 1
    c.execute('INSERT INTO Follower(user_id, user_name, following) VALUES(%s,%s,%s)', (user_id, session['email'], check))
    sq.connection.commit()

    flash(session['email'] + ' Followed User', 'info')
    return redirect(url_for('profile', user_id=user_id))


# leave group
def unfollow(user_id):
    c = sq.connection.cursor()
    c.execute('UPDATE Follower SET following=0 WHERE user_id = %s AND user_name=%s', (user_id, session['email']))
    sq.connection.commit()

    flash(session['email'] + ' Unfollowed User', 'info')
    return redirect(url_for('profile', user_id=user_id))


# was memeber of this group func
def was_follower(user_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT following, user_name, user_id FROM Follower WHERE user_name=%s AND user_id=%s AND following=0', (session['email'], user_id))
    was = c.fetchone()
    if result > 0:
        if was.get('following') == 0:
            print('Was Following')
            return True
        else:
            return False

    else:
        return follow_user(user_id)

class PostForm(Form):
    post = TextAreaField('Post', [validators.length(max=250)])




def create(form):
    post = form.post.data
    c = sq.connection.cursor()
    c.execute('INSERT INTO Posts(body, author) VALUES(%s,%s)', (post, session['email']))
    sq.connection.commit()
    c.close()

    return redirect(url_for('posts'))



def get_posts():
    c = sq.connection.cursor()
    c.execute('SELECT * FROM Posts')
    blog = c.fetchall()
    c.close()

    return render_template('user/posts.html', blog=blog)

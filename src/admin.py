from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
import pymysql
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
from functools import wraps
import sq




def is_admin():
    current_role = session['role']
    print(current_role)
    if current_role:
        if current_role == 'admin':
            return True
        elif current_role == 'user':
            return False
    else:
        return 'User Unauthorized'


def admin_dashboard():
    c = sq.connection.cursor()
    c.execute('SELECT * FROM User WHERE role="user"')
    users = c.fetchall()
    c.execute('SELECT * FROM Groups_table')
    groups = c.fetchall()
    c.execute('SELECT * FROM Events')
    events = c.fetchall()
    return render_template('admin/admin.html', message="I am admin", users=users, groups=groups, events=events)



def admin_register(form):
    fname = form.fname.data
    lname = form.lname.data
    email = form.email.data
    password = sha256_crypt.encrypt(str(form.password.data))
    role = 'admin'

    c = sq.connection.cursor()

    c.execute('INSERT INTO User(first_name, last_name, email, password, role) VALUES(%s, %s, %s, %s, %s)', (fname, lname, email, password, role))

    sq.connection.commit()

    c.close()

    flash('you are now registered and can log in', 'info')

    return render_template('user/login.html', form=form)


def ban(user_id):
    c = sq.connection.cursor()
    c.execute('DELETE FROM User WHERE user_id = %s', [user_id])
    sq.conenction.commit()

    c.close()

    return redirect(url_for('admin_only'))

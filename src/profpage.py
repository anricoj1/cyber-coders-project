from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
import src.sql_connection
from passlib.hash import sha256_crypt
from functools import wraps
import sq

class prof_edit(Form):
    fname = StringField('First', [validators.length(min=1, max=50)])
    lname = StringField('Last', [validators.length(min=1, max=50)])
    email = StringField('Email', )

def display_prof():
    c = sq.connection.cursor()
    c.execute('SELECT g.group_id, a.group_id, name, user_name, tag, creator, attending FROM Groups_table g INNER JOIN Attendee a ON a.group_id=g.group_id WHERE user_name = %s AND attending = 1', [session['email']])
    groups = c.fetchall()

    return render_template('user/account.html', groups=groups)

#def edit_prof(Form):

from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
import pymysql
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
import sq

#search results, form called on homepage search_type is to filter searches
def search_results(form):
    results = []
    search_string = form.data['search']
    search_type = form.data['select']

    likeString = '%%' + search_string + '%%'

    c = sq.connection.cursor()
    if search_type == 'users':
        c.execute('SELECT * FROM User WHERE email LIKE %s', [likeString])
        users = c.fetchall()

        return render_template('base/home.html', users=users, form=form, search_type=search_type)
    elif search_type == 'events':
        c.execute('SELECT * FROM Events WHERE name LIKE %s', [likeString])
        events = c.fetchall()

        return render_template('base/home.html', events=events, form=form, search_type=search_type)
    elif search_type == 'groups':
        c.execute('SELECT * FROM Groups_table WHERE name LIKE %s', [likeString])
        groups = c.fetchall()

        return render_template('base/home.html', groups=groups, form=form, search_type=search_type)
    else:
        return render_template('base/home.html', form=form)


def search_discover(form):
    results = []
    search_string = form.data['search']
    search_type = form.data['select']

    likeString = '%%' + search_string + '%%'

    c = sq.connection.cursor()
    if search_type == 'users':
        type = 'Users'
        c.execute('SELECT * FROM User WHERE email LIKE %s', [likeString])
        users = c.fetchall()

        return render_template('user/view.html', users=users, form=form, search_type=search_type, type=type)
    elif search_type == 'events':
        type = 'Events'
        c.execute('SELECT * FROM Events WHERE name LIKE %s', [likeString])
        events = c.fetchall()

        return render_template('user/view.html', events=events, form=form, search_type=search_type, type=type)
    elif search_type == 'groups':
        type = 'Groups'
        c.execute('SELECT * FROM Groups_table WHERE name LIKE %s', [likeString])
        groups = c.fetchall()

        return render_template('user/view.html', groups=groups, form=form, search_type=search_type, type=type)
    else:
        type = 'Discover'
        return render_template('user/view.html', form=form, type=type)

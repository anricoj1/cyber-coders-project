from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
import pymysql
from wtforms.validators import DataRequired
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, TimeField, validators
from wtforms.fields.html5 import DateField
from functools import wraps
import sq

class CreateEvent(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    meetup = DateField('Date', format='%Y-%m-%d')
    starttime = TimeField('Start', format='%hh:%mm:%tt')
    endtime = TimeField('End', format='%hh:%mm:%tt')
    location = StringField('Location', )
    description = TextAreaField('Description', )


# creating an event function required fields (form, group_id (specifies group), event)
def event_create(form, group_id, event):
    name = form.name.data
    meetup = form.meetup.data
    starttime = form.starttime.data
    endtime = form.endtime.data
    location = form.location.data
    description = form.description.data

    c = sq.connection.cursor()
    c.execute('INSERT INTO Events(name, date_time, starttime, endtime, location, description, creator, group_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (name, meetup, starttime, endtime, location, description, session['email'], [group_id]))

    sq.connection.commit()

    c.close()

    flash('Event Created', 'info')
    return redirect(url_for('dashboard'))


# view event function reuires event_id
def fetch_event(event_id):
    c = sq.connection.cursor()
    c.execute('SELECT * FROM Events WHERE event_id = %s', [event_id])
    event = c.fetchone()
    c.execute('SELECT COUNT(attending) FROM Attendee WHERE attending=1 and event_id = %s', event_id)
    a = c.fetchone()
    count = a.get('COUNT(attending)')
    c.execute('SELECT user_name FROM Attendee WHERE attending=1 and event_id = %s', event_id)
    attendee = c.fetchall()
    c.execute('SELECT user_name, attending FROM Attendee WHERE attending=1 AND event_id = %s AND user_name=%s', (event_id, session['email']))
    mem = c.fetchone()

    return render_template('events/event.html', event=event, count=count, attendee=attendee, mem=mem)


def get_attendees(event_id):
    c = sq.connection.cursor()
    c.execute('SELECT user_name, event_id, attending FROM Attendee WHERE event_id = %s', event_id)
    recip = c.fetchall()
    recipients = []
    for r in recip:
        attendee = r.get('user_name')
        recipients.append(attendee)

    return recipients

# delete event requires event_id (must be creator)
def remove_event(event_id):
    c = sq.connection.cursor()

    c.execute('DELETE FROM Events WHERE event_id = %s', [event_id])
    c.execute('DELETE FROM Attendee WHERE event_id = %s', [event_id])

    sq.connection.commit()

    c.close()

    flash('Event Deleted', 'info')

    return redirect(url_for('dashboard'))

# join group, is called in main project file
def join_event(event_id):
    c = sq.connection.cursor()
    check = 1
    c.execute('INSERT INTO Attendee(event_id, user_name, attending) VALUES(%s,%s,%s)', (event_id, session['email'], check))
    sq.connection.commit()

    flash(session['email'] + ' Joined Event', 'info')
    return redirect(url_for('event', event_id=event_id))


# leave group
def leave_event(event_id):
    c = sq.connection.cursor()
    c.execute('UPDATE Attendee SET attending=0 WHERE event_id = %s AND user_name=%s', (event_id, session['email']))
    sq.connection.commit()

    flash(session['email'] + ' Left Group', 'info')
    return redirect(url_for('event', event_id=event_id))


# was memeber of this group func
def was_attendee(event_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT attending, user_name, event_id FROM Attendee WHERE user_name=%s AND event_id=%s AND attending=0', (session['email'], event_id))
    was = c.fetchone()
    if result > 0:
        if was.get('attending') == 0:
            print('Was Attendee')
            return True
        else:
            return False

    else:
        return join_event(event_id)


def is_creator(event_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT event_id, creator FROM Events WHERE event_id = %s', [event_id])
    creator = c.fetchone()
    if result > 0:
        if session['email'] == creator.get('creator'):
            return True
        else:
            return False
    else:
        return 'Unauthorized'

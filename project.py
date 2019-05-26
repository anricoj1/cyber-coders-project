from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging, jsonify
from wtforms import Form, RadioField, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from flask_mail import Mail, Message
import pymysql
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from functools import wraps
from src.base import *
from src.user import *
from src.profpage import display_prof
from src.groups import *
from src.events import *
from src.admin import *
import sq
import smtplib


app = Flask(__name__)
app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME= 'MEETCSC330@gmail.com',
        MAIL_PASSWORD= 'MeetMe330'
    )


mail = Mail(app)


#join event/group form (needs if else to determine if user sumbmitted this form or not)
class Check(Form):
    join = BooleanField('Join', validators=[DataRequired(), ])


class SignUpForm(Form):
    fname = StringField('First', [validators.length(min=1, max=50)])
    lname = StringField('Last', [validators.length(min=1, max=50)])
    email = StringField('Email', )
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords dont match')
    ])
    confirm = PasswordField('Confirm Password')

#search class filters(users,events,groups)
class SearchFor(Form):
    choices = [('users', 'Users'),
               ('events', 'Events'),
               ('groups', 'Groups')]
    select = RadioField('Filter By', choices=choices)
    search = StringField('')


#top level route homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    c = sq.connection.cursor()
    form = SearchFor(request.form)
    if request.method == 'POST' and form.validate():
        flash('Performed a Search', 'info')
        return search_discover(form)
    else:
        c = sq.connection.cursor()
        c.execute('SELECT * FROM Groups_table')
        groups = c.fetchall()
        return render_template('base/home.html', form=form, groups=groups)


# User regisry section
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        return sign(form)
    else:
        return render_template('user/signup.html', form=form)


# user login, user logs in from email
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return log()
    else:
        return render_template('user/login.html')


#logout route, clears session
@app.route('/logout')
@is_logged_in
def logout():
    return lout()


#admin only route role must be admin
@app.route('/admin_only')
@is_logged_in
def admin_only():
    if is_admin():
        return admin_dashboard()
    else:
        return render_template('admin/Unauthorized.html')


#user dashboard (basic user info)
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    flash(session['first_name'] + ' Your Dashboard Lets You Manage Your Meets!', 'info')
    if is_admin():
        return admin_dashboard()
    else:
        return dash()


#to visit another users profile
@app.route('/profile/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def profile(user_id):
    return user_profile(user_id)


#view your profile (uses session)
@app.route('/account', methods=['GET', 'POST'])
@is_logged_in
def account():
    return display_prof()


#admins can create another admin account
@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if is_admin():
        form = SignUpForm(request.form)
        if request.method == 'POST' and form.validate():
            return admin_register(form)
        else:
            return render_template('admin/a_reg.html', form=form)
    else:
        return render_template('admin/Unauthorized.html')

# creating group form (name, tag, groupIMG)
class CreateGroup(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    tag = StringField('Tag', )
    description = TextAreaField('Description', )
    GroupIMG = FileField('GroupIMG', )


# route for creating a group requires INSERT
@app.route('/create_group', methods=['GET', 'POST'])
@is_logged_in
def start_group():
    form = CreateGroup(request.form)
    if request.method == 'POST' and form.validate():
        return group_create(form)
    else:
        return render_template('groups/add_group.html', form=form)


#group page requires group_id
@app.route('/group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def group(group_id):
    c = sq.connection.cursor()
    c.execute('SELECT * FROM Groups_table WHERE group_id = %s', [group_id])
    group = c.fetchone()
    c.execute('SELECT COUNT(attending) FROM Attendee WHERE attending=1 and group_id = %s', group_id)
    a = c.fetchone()
    count = a.get('COUNT(attending)')
    return retrieve_events(group, count, group_id)


#follow/join group (if else for group.html to change buttons)
@app.route('/follow_group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_group(group_id):
    if was_member(group_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Attendee SET attending = 1 WHERE user_name = %s AND group_id = %s', (session['email'], group_id))
        sq.connection.commit()
        flash(session['first_name'] + ' Joined Group', 'info')
        return redirect(url_for('group', group_id=group_id))
    else:
        return join_group(group_id)


#unfollow/leave group (if else in group.html)
@app.route('/unfollow_group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_group(group_id):
    return leave_group(group_id)


# starting event calls CreateEvent Form, requires event_create and group_id (interest Group)
@app.route('/start_event/<string:group_id>', methods=['GET', 'POST'])
def start_event(group_id):
    form = CreateEvent(request.form)
    if request.method == 'POST' and form.validate():
        return event_create(form, group_id, event)
    else:
        return render_template('events/add_event.html', form=form)



# Creator and admin have priveleges to delete group (no one else)
@app.route('/delete_group/<string:group_id>', methods=['POST'])
@is_logged_in
def delete_group(group_id):
    if is_admin():
        delete_group_noto(group_id)
        return remove_group(group_id)
    elif is_owner(group_id):
        delete_group_noto(group_id)
        return remove_group(group_id)
    else:
        return render_template('admin/Unauthorized.html')


# Event Form
class CreateEvent(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    meetup = DateField('Date', format='%Y-%m-%d')
    starttime = TimeField('Start', )
    endtime = TimeField('End', )
    location = StringField('Location', )
    description = TextAreaField('Description', )


#view event route
@app.route('/event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def event(event_id):
    return fetch_event(event_id)



#follw/join event (if else in event.html)
@app.route('/follow_event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_event(event_id):
    if was_attendee(event_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Attendee SET attending = 1 WHERE user_name = %s AND event_id = %s', (session['email'], event_id))
        sq.connection.commit()
        flash(session['first_name'] + ' Joined Event', 'info')
        return redirect(url_for('event', event_id=event_id))
    else:
        return join_event(event_id)


#unfollow/leave event (if else in event.html)
@app.route('/unfollow_event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_event(event_id):
    return leave_event(event_id)



#edit profile (in progresss) requires is_current(user_id) or Unauthorized
@app.route('/edit_profile/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_profile(user_id):
    if is_current(user_id):
        return modify_profile(user_id)
    else:
        return render_template('admin/Unauthorized.html')



# deleting an event route Requires DELETE, uses POST
@app.route('/delete_event/<string:event_id>', methods=['POST'])
@is_logged_in
def delete_event(event_id):
    if is_admin():
        delete_event_noto(event_id)
        return remove_event(event_id)
    elif is_creator(event_id):
        delete_event_noto(event_id)
        return remove_event(event_id)
    else:
        return render_template('admin/Unauthorized.html')


#discover profiles, events, and groups. Maybe can be converted to some sort of feed
@app.route('/search', methods=['GET', 'POST'])
def viewall():
    form = SearchFor(request.form)
    if request.method == 'POST' and form.validate():
        return search_discover(form)
    else:
        return search(form)




#delete/ban account takes is_admin and is_current
@app.route('/delete_profile/<string:user_id>', methods=['GET', 'POST'])
def ban_user(user_id):
    if is_admin():
        return ban(user_id)
    elif is_current(user_id):
        return redirect(url_for('secondchance'))
    else:
        return render_template('admin/Unauthorized.html')


#give user second chance before proceeding to delete account
@app.route('/secondchance', methods=['GET', 'POST'])
def secondchance():
    return render_template('secondchance.html')



#edit user role priveleges (is_admin)
@app.route('/edit_priv/<string:user_id>', methods=['GET', 'POST'])
def edit_priv(user_id):
    if is_admin():
        c = sq.connection.cursor()
        c.execute('UPDATE User SET role="admin" WHERE user_id = %s', [user_id])
        return redirect(url_for('admin_only'))
    else:
        return render_template('admin/Unauthorized.html')





# creator has access to editing the event
@app.route('/edit_event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_event(event_id):
    if is_creator(event_id):
        c = sq.connection.cursor()

        result = c.execute('SELECT * FROM Events WHERE event_id = %s', [event_id])

        event = c.fetchone()
        c.close()

        form = CreateEvent(request.form)

        form.name.data = event['name']
        form.meetup.strftime = event['date_time']
        form.starttime.strftime = event['starttime']
        form.endtime.strftime = event['endtime']
        form.location.data = event['location']
        form.description.data = event['description']

        if request.method == 'POST' and form.validate():
            name = request.form['name']
            meetup = request.form['meetup']
            starttime = request.form['starttime']
            endtime = request.form['endtime']
            location = request.form['location']
            description = request.form['description']

            c = sq.connection.cursor()

            c.execute('UPDATE Events SET name=%s, date_time=%s, starttime=%s, endtime=%s, location=%s, description=%s WHERE event_id=%s', (name, meetup, starttime, endtime, location, description, event_id))

            sq.connection.commit()

            c.execute('SELECT starttime, endtime FROM Events WHERE event_id = %s', event_id)
            times = c.fetchone()


            c.close()

            attend = get_attendees(event_id)

            if attend == []:
                return redirect(url_for('dashboard'))

            else:
                edit_event_noto(event_id, form, attend, times)
                flash('Event Updated, Notificaton Sent!', 'info')
                return redirect(url_for('index'))
        else:
            return render_template('events/add_event.html', form=form)
    else:
        return render_template('admin/Unauthorized.html')


# Edit a groups form, requires a SELECT and UPDATE uses GET and POST
@app.route('/edit_group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_group(group_id):
    if is_owner(group_id):
        c = sq.connection.cursor()
        result = c.execute('SELECT * FROM Groups_table WHERE group_id = %s', [group_id])

        group = c.fetchone()
        c.close()

        form = CreateGroup(request.form)

        form.name.data = group['name']
        form.tag.data = group['tag']
        form.description.data = group['group_description']
        form.GroupIMG.data = group['group_img_path']

        if request.method == 'POST' and form.validate():
            name = request.form['name']
            tag = request.form['tag']
            description = request.form['description']
            GroupIMG = request.form['GroupIMG']

            c = sq.connection.cursor()

            c.execute('UPDATE Groups_table SET name=%s, tag=%s, group_description=%s, group_img_path=%s WHERE group_id=%s', (name, tag, description, GroupIMG, group_id))
            sq.connection.commit()

            c.close()


            attend = get_members(group_id)

            if attend == []:
                return redirect(url_for('dashboard'))

            else:
                edit_group_noto(group_id, form, attend)
                flash('Group Updated, Notificaton Sent', 'info')
                return redirect(url_for('dashboard'))
        else:
            return render_template('groups/add_group.html', form=form)
    else:
        return render_template('admin/Unauthorized.html')


# delete group Notificaton
def delete_group_noto(group_id):
    c = sq.connection.cursor()
    c.execute('SELECT name FROM Groups_table WHERE group_id = %s', group_id)
    group = c.fetchone()
    mems = get_members(group_id)
    if mems == []:
        return redirect(url_for('dashboard'))
    else:
        msg = Message('Notifications For You',
                          sender=session['email'],
                          recipients=mems)

        msg.body = 'Group ' + str(group.get('name')) + ' Has Been Removed'
        mail.send(msg)

        return msg

#delete event Notificaton
def delete_event_noto(event_id):
    c = sq.connection.cursor()
    c.execute('SELECT name FROM Events WHERE event_id = %s', event_id)
    event = c.fetchone()
    mems = get_attendees(event_id)
    if mems == []:
        return redirect(url_for('dashboard'))

    else:
        msg = Message('Notifications For You',
                          sender=session['email'],
                          recipients=mems)

        msg.body = 'Event ' + str(event.get('name')) + ' Has Been Cancelled'
        mail.send(msg)

        return msg


#edit group Notificaton
def edit_group_noto(group_id, form, attend):
    msg = Message('Notifications For You!',
                sender=session['email'],
                recipients=attend)

    msg.body = 'Your Meet Group ' + form.name.data + ' Has Made A Change ' + form.description.data

    mail.send(msg)

    return msg

#edit event Notificaton
def edit_event_noto(event_id, form, attend, times):
    msg = Message('Notifications For You!',
                sender=session['email'],
                recipients=attend)

    msg.body = 'A Meet Event: ' + form.name.data + ' ON: ' + form.meetup.strftime + ' From: ' + str(times.get('starttime')) + ' - ' + str(times.get('endtime')) + ' AT ' + form.location.data

    mail.send(msg)

    return msg


if __name__ == '__main__':
    app.secret_key='meet2'
    app.run(debug=True)

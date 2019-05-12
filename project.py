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
from src.base import search_results, search_discover
from src.user import sign, log, lout, is_logged_in, dash, search, user_profile, modify_profile, is_current
from src.profpage import display_prof
from src.groups import group_create, join_group, retrieve_events, remove_group, get_members, leave_group, was_member, is_owner
from src.events import remove_event, fetch_event, event_create, join_event, get_attendees, was_attendee, leave_event, is_creator
from src.follow import follow, unfollow, was_follower, create, get_posts
from src.admin import is_admin, admin_dashboard, ban, admin_register
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
        return render_template('admin/admin.html', message="I am admin")
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


@app.route('/follow_group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_group(group_id):
    if was_member(group_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Attendee SET attending = 1 WHERE user_name = %s AND group_id = %s', (session['email'], group_id))
        sq.connection.commit()
        flash(session['email'] + ' Joined Group', 'info')
        return redirect(url_for('group', group_id=group_id))
    else:
        return redirect(url_for('group', group_id=group_id))



@app.route('/unfollow_group/<string:group_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_group(group_id):
    return leave_group(group_id)


# starting event calls CreateEvent Form, requires event_create
@app.route('/start_event/<string:group_id>', methods=['GET', 'POST'])
def start_event(group_id):
    form = CreateEvent(request.form)
    if request.method == 'POST' and form.validate():
        return event_create(form, group_id, event)
    else:
        return render_template('events/add_event.html', form=form)



# Creator has option to delete group if neccessary uses POST
@app.route('/delete_group/<string:group_id>', methods=['POST'])
@is_logged_in
def delete_group(group_id):
    c = sq.connection.cursor()
    c.execute('SELECT name FROM Groups_table WHERE group_id = %s', group_id)
    group = c.fetchone()
    mems = get_members(group_id)
    msg = Message('Notifications For You',
                   sender=session['email'],
                   recipients=mems)
    msg.body = 'Group ' + str(group.get('name')) + ' Has Been Removed'
    return remove_group(group_id)


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




@app.route('/follow_event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_event(event_id):
    if was_attendee(event_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Attendee SET attending = 1 WHERE user_name = %s AND event_id = %s', (session['email'], event_id))
        sq.connection.commit()
        return redirect(url_for('event', event_id=event_id))
    else:
        return join_event(event_id)



@app.route('/unfollow_event/<string:event_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_event(event_id):
    return leave_event(event_id)



@app.route('/edit_profile/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def edit_profile(user_id):
    if is_current(user_id):
        return modify_profile(user_id)
    else:
        return render_template('admin/Unauthorized.html')




@app.route('/follow_user/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def follow_user(user_id):
    if follow(user_id):
        c = sq.connection.cursor()
        c.execute('UPDATE Follower SET following = 1 WHERE user_name = %s AND user_id = %s', (session['email'], user_id))
        sq.connection.commit()
        return redirect(url_for('profile', user_id=user_id))
    else:
        return follow_user(user_id)



@app.route('/unfollow_user/<string:user_id>', methods=['GET', 'POST'])
@is_logged_in
def unfollow_user(user_id):
    return unfollow(user_id)


class PostForm(Form):
    post = TextAreaField('Post', [validators.length(max=250)])


@app.route('/post', methods=['GET', 'POST'])
@is_logged_in
def post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        return create(form)
    else:
        return render_template('user/post.html', form=form)




@app.route('/posts', methods=['GET', 'POST'])
@is_logged_in
def posts():
    return get_posts()




@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if validate_email():
        return render_template('admin/Unauthorized.html')
    else:
        return render_template('admin/Unauthorized.html')


# deleting an event route Requires DELETE, uses POST
@app.route('/delete_event/<string:event_id>', methods=['POST'])
@is_logged_in
def delete_event(event_id):
    c = sq.connection.cursor()
    c.execute('SELECT name FROM Events WHERE event_id = %s', event_id)
    event = c.fetchone()
    attend = get_attendees(event_id)
    msg = Message('Notifications For You',
                   sender=session['email'],
                   recipients=attend)
    msg.body = 'Event ' + str(event.get('name')) + ' Has Been Cancelled'
    mail.send(msg)
    return remove_event(event_id)


#discover profiles, events, and groups. Maybe can be converted to some sort of feed
@app.route('/search', methods=['GET', 'POST'])
def viewall():
    form = SearchFor(request.form)
    if request.method == 'POST' and form.validate():
        return search_discover(form)
    else:
        return search(form)













@app.route('/delete_profile/<string:user_id>', methods=['GET', 'POST'])
def ban_user(user_id):
    if is_admin():
        return ban(user_id)
    else:
        return redirect(url_for('secondchance'))


@app.route('/secondchance', methods=['GET', 'POST'])
def secondchance():
    return render_template('secondchance.html')








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

            msg = Message('Notifications For You!',
                        sender=session['email'],
                        recipients=attend)

            msg.body = 'A Meet Event: ' + form.name.data + ' ON: ' + form.meetup.strftime + ' From: ' + str(times.get('starttime')) + ' - ' + str(times.get('endtime')) + ' AT ' + form.location.data

            mail.send(msg)

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

            msg = Message('Notifications For You!',
                        sender=session['email'],
                        recipients=attend)

            msg.body = 'Your Meet Group ' + form.name.data + ' Has Made A Change ' + form.description.data

            mail.send(msg)

            flash('Group Updated, Notificaton Sent', 'info')
            return redirect(url_for('index'))
        else:
            return render_template('groups/add_group.html', form=form)
    else:
        return render_template('admin/Unauthorized.html')


if __name__ == '__main__':
    app.secret_key='meet2'
    app.run(debug=True)

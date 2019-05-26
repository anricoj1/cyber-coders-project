from flask import Flask, render_template, redirect, url_for, request, flash, session, request, logging
import pymysql
from wtforms.validators import DataRequired
from wtforms import Form, StringField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField, PasswordField, FileField, validators
from functools import wraps
import sq


class Check(Form):
    join = BooleanField('Join', validators=[DataRequired(), ])

class CreateGroup(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    tag = StringField('Tag', )
    description = TextAreaField('Description', )
    GroupIMG = FileField('GroupIMG', )

# create group
def group_create(form):
    name = form.name.data
    tag = form.tag.data
    description = form.description.data
    GroupIMG = form.GroupIMG.data


    c = sq.connection.cursor()

    c.execute('INSERT INTO Groups_table(name, tag, group_description, group_img_path, creator) VALUES(%s, %s, %s, %s, %s)', (name, tag, description, GroupIMG, session['email']))

    sq.connection.commit()

    flash('Group Created', 'info')

    return redirect(url_for('dashboard'))


# join group, is called in main project file
def join_group(group_id):
    c = sq.connection.cursor()
    check = 1
    c.execute('INSERT INTO Attendee(group_id, user_name, attending) VALUES(%s,%s,%s)', (group_id, session['email'], check))

    sq.connection.commit()

    flash(session['email'] + ' Joined Group', 'info')
    return redirect(url_for('group', group_id=group_id))


# leave group
def leave_group(group_id):
    c = sq.connection.cursor()
    c.execute('UPDATE Attendee SET attending=0 WHERE group_id = %s AND user_name=%s', (group_id, session['email']))
    sq.connection.commit()

    flash(session['email'] + ' Left Group', 'info')
    return redirect(url_for('group', group_id=group_id))


# was memeber of this group func
def was_member(group_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT attending, user_name, group_id FROM Attendee WHERE user_name=%s AND group_id=%s AND attending=0', (session['email'], group_id))
    was = c.fetchone()
    if result > 0:
        if was.get('attending') == 0:
            print('Was Member')
            return True
        else:
            return False

    else:
        return join_group(group_id)


# retrieving events under a specific group
def retrieve_events(group, count, group_id):
    c = sq.connection.cursor()
    c.execute('SELECT * FROM Events WHERE group_id = %s', [group_id])
    event = c.fetchall()

    c.execute('SELECT user_name, attending FROM Attendee WHERE group_id=%s and attending=1 AND user_name=%s', (group_id, session['email']))
    mem = c.fetchone()
    print(mem)

    return render_template('groups/group.html', event=event, group=group, count=count, mem=mem)



# delete group function
def remove_group(group_id):
    c = sq.connection.cursor()
    c.execute('DELETE FROM Groups_table WHERE group_id = %s', [group_id])
    c.execute('DELETE FROM Attendee WHERE group_id = %s', [group_id])

    sq.connection.commit()

    c.close()

    flash('Group Deleted', 'info')

    return redirect(url_for('dashboard'))


#get recipients for notifications
def get_members(group_id):
    c = sq.connection.cursor()
    c.execute('SELECT user_name, group_id, attending FROM Attendee WHERE group_id = %s', group_id)
    recip = c.fetchall()
    recipients = []
    for r in recip:
        attendee = r.get('user_name')
        recipients.append(attendee)

    return recipients


#verify owner of group 
def is_owner(group_id):
    c = sq.connection.cursor()
    result = c.execute('SELECT group_id, creator FROM Groups_table WHERE group_id = %s', [group_id])
    creator = c.fetchone()
    if result > 0:
        if session['email'] == creator.get('creator'):
            return True
        else:
            return False
    else:
        return 'Unauthorized'

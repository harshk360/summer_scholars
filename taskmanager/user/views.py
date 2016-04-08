# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from wtforms.ext.appengine.db import model_form
from taskmanager.user.forms import CreateEventForm
from taskmanager.user.models import RecEvent, User
from taskmanager.utils import flash_errors
from taskmanager.extensions import db

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')

@blueprint.route('/recruiting/')
@login_required
def recruiting():
    """List recruiting events."""
    events = RecEvent.query.all()
    for event in events:
        event.volunteer_list = []
        if event.volunteers:
            for user in event.volunteers:
                event.volunteer_list.append(user.full_name)
    return render_template('users/recruiting.html', events = events)

@blueprint.route('/recruiting/create/', methods=['GET', 'POST'])
@login_required
def create():
    """Create new event."""
    form = CreateEventForm(request.form, csrf_enabled=False)
    print ("form received")
    if form.validate_on_submit():
        print ("valid")
        RecEvent.create(title=form.title.data, date=form.date.data, time=form.time.data)
        flash('You have successfully created a new recruiting event.', 'success')
        return redirect(url_for('user.recruiting'))
    else:
        flash_errors(form)
    return render_template('users/create_event.html', form=form)

@blueprint.route('/recruiting/volunteer/<event_id>', methods=['GET', 'POST'])
@login_required
def volunteer(event_id):
    event = RecEvent.query.filter_by(id=event_id).first()
    if current_user in event.volunteers:
        event.volunteers.remove(current_user)
        db.session.add(event)
        db.session.commit()
    else:
        event.volunteers.append(current_user)
        db.session.add(event)
        db.session.commit()

    return redirect(url_for('user.recruiting'))

# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import DateField
from wtforms_components import DateField, TimeField


from .models import User


class RegisterForm(Form):
    """Register form."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=25)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True

class CreateEventForm(Form):
    """Create recruiting event form."""
    title = StringField('Event Title', validators=[DataRequired(), Length(min=3, max=80)])
    date = DateField('Date')
    time = TimeField('Time')
    location = StringField('Event Location', validators=[Length(min=0, max=80)])
    contact_person = StringField('Contact Person', validators=[Length(min=0, max=80)])


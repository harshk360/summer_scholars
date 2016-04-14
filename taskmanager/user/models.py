# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from taskmanager.database import Column, Model, SurrogatePK, db, reference_col, relationship
from taskmanager.extensions import bcrypt

volunteers = db.Table('volunteers',
    db.Column('event_id', db.Integer, db.ForeignKey('rec_events.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, first_name=None, last_name=None, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, first_name=first_name, last_name=last_name, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def get_id(self):
        return self.id

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

class RecEvent(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'rec_events'
    title = Column(db.String(80), unique=False, nullable=False)
    date = Column(db.Date, nullable=True)
    time = Column(db.Time, nullable=True)
    location = Column(db.String(80), unique=False, nullable=True)
    contact_person = Column(db.String(80), unique=False, nullable=True)
    volunteers = db.relationship(User, secondary=volunteers, lazy='dynamic', backref=db.backref('RecEvent', lazy='dynamic'))


    def __init__(self, title, date, time, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, date=date, time=time, **kwargs)

    @property
    def title_date(self):
        """Title and time."""
        return '{0} {1}'.format(self.title, self.date)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Event({title!r})>'.format(title=self.title)
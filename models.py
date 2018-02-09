# python imports
import datetime
import sys

# flask bcrypt for passwords
from flask_bcrypt import generate_password_hash, check_password_hash

# basic peewee import style
from peewee import *

# magic from flask_login
from flask_login import UserMixin

DATABASE = SqliteDatabase('application.db')

# model definitions
class BaseModel(Model):
    class Meta:
        database = DATABASE


class User(UserMixin, BaseModel):
    """User is the user entity model"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    firstname = CharField()
    lastname = CharField()
    is_admin = BooleanField(default=False)
    joined_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create_user(cls, username, email, password, firstname='', lastname='', is_admin=False):
        hashed_password = generate_password_hash(password)
        try:
            with DATABASE.transaction():
                cls.create(username=username, firstname=firstname, lastname=lastname, email=email,
                           password=hashed_password, is_admin=is_admin)
        except IntegrityError:
            raise ValueError('username or email already exists')
        
    def authenticate(self, password):
        if check_password_hash(self.password, password):
            return True
        return False

    def reset_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def __repr__(self):
        return self.username

def initialize_database():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)


def audit_users():
    """audits user table for unencrypted passwords, and fixes them"""
    users = User.select()
    for user in users:
        try:
            user.authenticate(user.password)
        except:
            user.reset_password(user.password)
            
def create_superuser():
    """console method to create an admin/superuser"""
    # not if using python3, change raw_input and print statements!
    # if you're reading this code, you already understand this.
    print ("Enter data for admin/superuser (all fields required)")
    if '2.7' in sys.version:
        username = raw_input("Enter username: ")
        email = raw_input("Enter email: ")
        password = raw_input("Enter password: ")
    else:
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")    
        
    try:
        User.create_user(username=username, email=email, password=password, is_admin=True)
    except Exception as e:
        print (e)
        print ("database probably needs to be created, please use --initdatabase command line switch")


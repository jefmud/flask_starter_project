# flask_starter_project
A flask starter project with user login, registration, administration, and Bootstrap -- featuring PeeWee ORM.

Currently compatible with Python 2.7.9 and higher.

NOT CURRENTLY COMPATIBLE WITH Python 3.x (something with Flask-wtf and WTF-peewee)

Be careful with library versions because they can get freaked out if dependencies aren't.  Play it safe and use virtualenv.

I reported some issues to Charles Leifer about Peewee (3.0) and Flask-Admin, so you may notice I am using his
earlier version of the library for now.

Requirements (and dependencies)

The major libraries are:
1. Flask
2. WTForms
3. Flask-admin
4. Flask-login
5. Flask-bcrypt
6. Flask-wtf
7. Peewee
8. wtf-peewee

```
pip freeze

bcrypt==3.1.4
cffi==1.11.4
click==6.7
dominate==2.3.1
Flask==0.12.2
Flask-Admin==1.5.0
Flask-Bcrypt==0.7.1
Flask-Bootstrap==3.3.7.1
Flask-Login==0.4.1
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
peewee==2.10.2
pycparser==2.18
six==1.11.0
visitor==0.1.3
Werkzeug==0.14.1
wtf-peewee==0.2.6
WTForms==2.1
```

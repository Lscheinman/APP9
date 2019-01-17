import os
import unittest

from flask_script import Manager
from flask import render_template
from flask import session, request, redirect, flash, url_for, jsonify
from app import blueprint
from app.main import create_app
from app.main.model import o_auth as oa
from app.main.model import messages as ms

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
auth = oa.o_auth()
messenger = ms.messenger()

inbox_menu_items = ['all', 'new', 'alerts', 'sent', 'read', 'deleted']


def load_models():
    # TODO if models goes beyond inbox, menus, and others then have a single place to load them if done from multiple urls
    return


def update_menu(active_item, menu_items):
    """
    Generate a dictionary that represents a model of a menu and highlights the
    active item in the menu
    :param active_item:
    :return:
    """
    inbox_model = {}
    for m in menu_items:
        if active_item == m:
            inbox_model[m] = 'breadcrumb-item active'
        else:
            inbox_model[m] = ''

    return inbox_model


def print_session():
    for s in session:
        print(s, session[s])


@app.route('/send_message', methods=['POST'])
def send_message():
    print("MESSAGE0", request.form)
    msg_id, status = messenger.create_message(sender=session['user']['username'],
                                      receiver=request.form['to_user'],
                                      subject=request.form['msg_subject'],
                                      body=request.form['msg_body'],
                                      category=request.form['msg_category']
                                      )
    print("MESSAGE1", msg_id, status)

    app_users = request.form['to_user']
    if "," in app_users:
        app_users = app_users.split(",")
        for user_name in app_users:
            to_id = messenger.get_user(user_name)
            r = messenger.send_message(msg_id=msg_id, to_id=to_id, from_id=session['user']['id'])
            print(r)
    else:
        print("MESSAGE2", app_users)
        to_id = messenger.get_user(app_users)
        print("MESSAGE3",to_id, session['user'])
        r = messenger.send_message(msg_id=msg_id, to_id=to_id, from_id=session['user']['id'])
        print("MESSAGE4", r)

    return redirect(url_for('messages'))

@app.route('/message_profile', methods=['POST', 'GET'])
def message_profile():
    #TODO tie this in with vatiables representing the maessage for a profile lookup
    message_profile_model = {'id': request.form['active_item']}
    print(message_profile_model)

    return render_template("uc-calendar.html", message_profile_model=message_profile_model, profile_picture="user1.png",)



@app.route('/refresh_inbox', methods=['POST', 'GET'])
def refresh_inbox():

    if request.method == 'POST':
        menu_model= update_menu(request.form['active_item'], inbox_menu_items)
        user_id = messenger.get_user(session['user']['username'])
        message_model = messenger.get_messages(user_id, session['user']['username'])
        message_profile_model = {'id': 0}

        if str(request.form['active_item']) != 'all':
            filtered_messages = []
            for m in message_model['messages']:
                if m['status'] == request.form['active_item']:
                    filtered_messages.append(m)
            if len(filtered_messages) < 1:
                filtered_messages = [{'body' : ('No %s messages' % request.form['active_item'])}]
            message_model['messages'] = filtered_messages

        return render_template("messages_active.html",
                               profile_picture="user1.png",
                               menu_model=menu_model,
                               message_model=message_model,
                               message_profile_model=message_profile_model)

    else:
        return redirect(url_for('messages'))


@app.route('/home')
def home():
    session['page_name'] = 'Home'
    return render_template("index.html", pagename='Home')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html", pagename='Login')
    elif request.method == 'POST':
        session['token'] = auth.login(email=request.form['email'], password=request.form['password'])
        if session['token']:
            session['user'] = auth.get_user(auth.get_user_name(request.form['email']))
            session['profile_picture'] = "user1.png"
            session['user']['id'] = messenger.get_user(session['user']['username'])
            message_profile_model = {'id': 0}
            message_model = messenger.get_messages(session['user']['id'], session['user']['username'])
            menu_model = update_menu("", inbox_menu_items)
            flash('You were successfully logged in')
            return render_template("messages.html", pagename='Messages',
                                   profile_picture="user1.png",
                                   message_model=message_model,
                                   message_profile_model=message_profile_model,
                                   menu_model=menu_model)


@app.route('/logout')
def logout():
    response = auth.logout(session['user']['username'], session['token'])
    session.pop("token")
    session.pop("user")
    # TODO flash message
    return render_template("login.html", pagename='Login', response=response)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html", pagename='Register')
    elif request.method == 'POST':
        if auth.create_user(username=request.form['username'],
                            email=request.form['email'],
                            password=request.form['password']):
            session['token'] = auth.encode_auth_token(request.form['username'])
            session['user'] = auth.get_user(auth.get_user_name(request.form['email']))
            user_id = messenger.get_user(request.form['username'])
            message_list = messenger.get_messages(user_id)
            return render_template("messages.html", pagename='Messages', messages=message_list)
        else:
            message = "Username or email has already been taken."
            return render_template("register.html", pagename='Register', message=message)


@app.route('/messages')
def messages():

    user_id = messenger.get_user(session['user']['username'])
    message_model = messenger.get_messages(user_id, session['user']['username'])
    menu_model = update_menu("", inbox_menu_items)
    message_profile_model = {'id': 0}

    return render_template("messages.html", pagename='Messages',
                           profile_picture="user1.png",
                           message_model=message_model,
                           menu_model=menu_model,
                           message_profile_model=message_profile_model)

@app.route('/calendar')
def calendar():
    return render_template("uc-calendar.html", pagename='Calendar')

@app.route('/profile')
def profile():
    return render_template("app-profile.html", pagename='Profile')


@manager.command
def run():
    app.run(host='0.0.0.0')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
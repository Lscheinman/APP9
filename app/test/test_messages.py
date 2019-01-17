from app.main.model import messages

msgr = messages.messenger()
tests = {}

users = [{'username': 'Tester','email': 'tester@email.com', 'profile_icon': 'user1.png'},
         {'username': 'Tester2', 'email': 'tester2@email.com', 'profile_icon': 'user2.png'},
         ]
messages = [{'receiver': 'Tester', 'sender': 'Tester2', 'subject': 'Newtest1', 'body': 'testing bodywdgwegewg', 'category': 'draft'},
            {'receiver': 'Tester2', 'sender': 'Tester', 'subject': 'NEwtest2', 'body': 'testing 1 bodyrgregregre', 'category': 'high'},
            {'receiver': 'Tester', 'sender': 'Tester2', 'subject': 'Newtest3', 'body': 'testing 2 bodyregrgregregre', 'category': 'alert'},
            ]

for u in users:
    tests['get_%s' % u['username']] = msgr.get_user(u['username'])
    if tests['get_%s' % u['username']] == False:
        print(msgr.create_user(u['username'], u['email'], u['username']))

for m in messages:
    tests['create_%s' % m['subject']], exists = msgr.create_message(receiver=m['receiver'], sender=m['sender'],
                                                                    subject=m['subject'], body=m['body'],
                                                                    category=m['category'])
    tests['send_%s' % m['subject']] = msgr.send_message(from_id=tests['get_%s' % m['sender']],
                                                        to_id=tests['get_%s' % m['receiver']],
                                                        msg_id=tests['create_%s' % m['subject']])
    tests['delete_%s' % m['subject']] = msgr.delete_message(user_id=tests['get_%s' % m['sender']],
                                                            msg_id=tests['create_%s' % m['subject']])
    tests['read_%s' % m['subject']] = msgr.open_message(user_id=tests['get_%s' % m['receiver']],
                                                          msg_id=tests['send_%s' % m['subject']])

for u in users:
    user_id = msgr.get_user(u['username'])
    tests['get_messages_%s' % u['username']] = msgr.get_messages(user_id, u['username'])

for t in tests:
    if 'get_messages' in str(t):
        for e in tests[t]:
            if str(e) == 'messages':
                for m in tests[t][e]:
                    if m['status'] != 'deleted':

                        print(m)
            else:
                print(e, tests[t][e])
    else:
        print(t, tests[t])
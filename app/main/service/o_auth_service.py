from app.main.model.o_auth import o_auth

oa = o_auth()
oa.open_db()


class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            token = oa.login(username=data.get('username'), password=data.get('password'))
            if token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'Authorization': token
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return response_object, 500

    @staticmethod
    def logout_user(auth_token, username):
        if auth_token:
            print(auth_token, username)
            response = oa.logout(username, auth_token)
            if response:
                response_object = {
                    'status': 'success',
                    'message': response
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Provide a valid username or token.'
                }
                return response_object, 402
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403


    @staticmethod
    def get_logged_in_user(request):
        # get the auth token
        try:
            auth_token = request.headers['Authorization']
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Provide Authorization in the headers. Missing %s ' % str(e)
            }
            return response_object, 401

        if auth_token:
            response = oa.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user = oa.get_user(response)
                if user['id'] is not None:
                    return user, 200

            response_object = {
                'status': 'fail',
                'message': response
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401

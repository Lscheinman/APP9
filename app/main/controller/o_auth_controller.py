from flask import request, session
from flask_restplus import Resource
from app.main.service.o_auth_service import Auth
from ..util.dto import OAuthDto

api = OAuthDto.api
user_auth = OAuthDto.user_auth
logout_parser = OAuthDto.oauth_parser


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @api.expect(logout_parser, validate=True)
    def post(self):
        # get auth token
        username = request.headers.get('username')
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(auth_header, username)
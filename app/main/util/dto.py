# Data Transfer Object (Dto)
from flask_restplus import Namespace, fields, reqparse

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

class OAuthDto:
    api = Namespace('oauth', description='OAuth authentication related operations')
    user_auth = api.model('oauth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
        'username': fields.String(required=True, description='The user email '),
    })
    oauth_parser = reqparse.RequestParser()
    oauth_parser.add_argument('Authorization', location='headers', required=True,
                        help="Session token for access verification")
    oauth_parser.add_argument('username', type=str, location='headers', required=True,
                        help="Unique username")


class OrientDto:
    api = Namespace('orient', description='OrientDB related operations', security='Bearer Auth', authorizations=authorizations)
    orient = api.model('orient', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
        'data': fields.String(required=True, description='The token identifying a valid user session'),
        'db_name':fields.String(required=False, description='Used to get information on a database or create a new one.')
    })
    person = api.model('person', {
        'e_fname': fields.String(required=True, description='Person first name, including middle if applicable'),
        'e_lname': fields.String(required=True, description='Person last name'),
        'e_gender': fields.String(required=False, description='Gender identity, male, female, or unknown'),
        'e_dob':fields.String(required=False, description='Date of birth YYYY-MM-DD'),
        'e_pob': fields.String(required=False, description='Place of birth as a description including'
                                                         ' geo coordinates if applicable'),
        'e_auth': fields.String(required=True, description='Variable for authentication access to data'),
        'db_name': fields.String(required=True, description='Database to insert the entity'),
        'headers': fields.String(requres=True, location='headers')
    })
    object = api.model('object', {
        'e_type': fields.String(required=True, description='Type of object such as document, language, social media...'),
        'e_category': fields.String(required=True, description='Category of object such as passport, french, twitter...'),
        'e_detail': fields.String(required=False, description='Description of the object'),
        'e_var1':fields.String(required=False, description='Variable placeholder such as follower count, character length...'),
        'e_var2': fields.String(required=False, description='Variable placeholder such as weight, time created...'),
        'e_var3': fields.String(required=False, description='Variable placeholder such as color, texture...'),
        'e_auth': fields.String(required=True, description='Variable for authentication access to data'),
        'db_name': fields.String(required=True, description='Database to insert the entity')
    })
    location = api.model('location', {
        'e_type': fields.String(required=True, description='Type of location such as point, area, landmark...'),
        'e_category': fields.String(required=True, description='Category of location such as home, room, commercial...'),
        'e_detail': fields.String(required=False, description='Description of the location'),
        'e_xcoord':fields.Float(required=False, description='Geo coordinate associated with Latitude'),
        'e_ycoord': fields.Float(required=False, description='Geo coordinate associated with Longitude'),
        'e_zcoord': fields.String(required=False, description='Variable placeholder such elevation, temperature...'),
        'e_postcode': fields.String(required=False, description='Reference to postal or zip codes'),
        'e_auth': fields.String(required=True, description='Variable for authentication access to data'),
        'db_name': fields.String(required=True, description='Database to insert the entity')
    })
    event = api.model('event', {
        'e_type': fields.String(required=True, description='Type of event such as birth, social media, call...'),
        'e_category': fields.String(required=True, description='Category of event such as human, tweet, or mobile phone...'),
        'e_detail': fields.String(required=False, description='Description of the event'),
        'e_date':fields.String(required=False, description='Date of the event in YYYY-MM-DD'),
        'e_time': fields.String(required=False, description='Local time of the event in HH:MM'),
        'e_var1': fields.String(required=False, description='Variable placeholder such as count of people involved, retweet count...'),
        'e_var2': fields.String(required=False, description='Variable placeholder such as duration, tags, related location...'),
        'e_var3': fields.String(required=False, description='Variable placeholder such as temperature, objects involved...'),
        'e_auth': fields.String(required=True, description='Variable for authentication access to data'),
        'db_name': fields.String(required=True, description='Database to insert the entity')
    })
    parser = reqparse.RequestParser()


    parser.add_argument('AUTH', type=str, required=True,
                        help="Variable for authentication access to data")

    parser.add_argument('db_name', type=str, required=True,
                        help="Database to insert the entity")

    p_parser = parser.copy()
    pole_parser = parser.copy()
    pole_parser.add_argument('Authorization', location='headers', required=True,
                        help="Session token for access verification")

    p_parser = pole_parser.copy()
    p_parser.add_argument('FNAME', type=str, required=False,
                          help="Person first name, including middle if applicable")
    p_parser.add_argument('LNAME', type=str, required=False,
                          help="Person last name")
    p_parser.add_argument('GENDER', type=str, required=False,
                          help="Gender identity, male, female, or unknown")
    p_parser.add_argument('DOB', type=str, required=False,
                          help="Date of birth YYYY-MM-DD")
    p_parser.add_argument('POB', type=str, required=False,
                          help="Place of birth as a description including geo coordinates if applicablen")
    o_parser = pole_parser.copy()
    o_parser.add_argument('TYPE', type=str, required=False,
                          help="Entity type. Highest level for taxonomy.")
    o_parser.add_argument('CATEGORY', type=str, required=False,
                          help="Entity category. 2nd level for taxonomy")
    o_parser.add_argument('DETAIL', type=str, required=False,
                          help="Description of the entity")
    l_parser = o_parser.copy()
    l_parser.add_argument('XCOORD', type=float, required=False,
                          help="Latitude geo coordinate equivalent")
    l_parser.add_argument('YCOORD', type=float, required=False,
                          help="Longitude geo coordinate equivalent")
    l_parser.add_argument('ZCOORD', type=str, required=False,
                          help="Other metric such as elevation")
    l_parser.add_argument('POSTCODE', type=str, required=False,
                          help="Postal or other zoning code")
    o_parser.add_argument('VAR1', type=str, required=False,
                          help="Entity variable information space 1")
    o_parser.add_argument('VAR2', type=str, required=False,
                          help="Entity variable information space 2")
    o_parser.add_argument('VAR3', type=str, required=False,
                          help="Entity variable information space 3")
    e_parser = o_parser.copy()
    e_parser.add_argument('DATE', type=str, required=False,
                          help="Date of the event in YYYY-MM-DD")
    e_parser.add_argument('TIME', type=str, required=False,
                          help="Time of the event in HH:MM")
    u_parser = e_parser.copy()
    u_parser.add_argument('GUID', type=str, required=True,
                          help="Unique identity to update")
    u_parser.add_argument('XCOORD', type=float, required=False,
                          help="Latitude geo coordinate equivalent")
    u_parser.add_argument('YCOORD', type=float, required=False,
                          help="Longitude geo coordinate equivalent")
    u_parser.add_argument('ZCOORD', type=str, required=False,
                          help="Other metric such as elevation")
    u_parser.add_argument('POSTCODE', type=str, required=False,
                          help="Postal or other zoning code")
    u_parser.add_argument('FNAME', type=str, required=False,
                          help="Person first name, including middle if applicable")
    u_parser.add_argument('LNAME', type=str, required=False,
                          help="Person last name")
    u_parser.add_argument('GENDER', type=str, required=False,
                          help="Gender identity, male, female, or unknown")
    u_parser.add_argument('DOB', type=str, required=False,
                          help="Date of birth YYYY-MM-DD")
    u_parser.add_argument('POB', type=str, required=False,
                          help="Place of birth as a description including geo coordinates if applicablen")

    m_parser = parser.copy()
    m_parser.add_argument('entity_a', type=str, required=True,
                          help="The entity that will remain after merging")
    m_parser.add_argument('entity_b', type=str, required=True,
                          help="The entity which will have its relationships associated with the remaining entity")

    d_parser = parser.copy()
    d_parser.add_argument('GUID', type=str, required=True,
                          help="The entity id to delete")

    r_parser = parser.copy()
    r_parser.add_argument('r_type', type=str, required=True,
                          help="Relationship type. If unknown, put related")
    r_parser.add_argument('r_source', type=str, required=True,
                          help="Unique ID of the source entity in the relationship")
    r_parser.add_argument('r_target', type=str, required=True,
                          help="Unique ID of the target entity in the relationship")
    r_parser.add_argument('r_var1', type=str, required=True,
                          help="Variable for the relationship such as weight or confidence")
    r_parser.add_argument('r_var2', type=str, required=True,
                          help="Variable for the relationship such as timestamp")

    s_parser = parser.copy()
    s_parser.add_argument('terms')

'''
class Client:
    api = Namespace('client', description='OAuth application client')
    client = api.model('client', {
        'client_id': fields.String(required=True, description='A random string'),
        'client_secret':fields.String(required=True, description='A random string'),
        'client_type': fields.String(required=True, description='Confidentiality'),
        'redirect_urls': fields.List(required=True, description='A list of redirect urls'),
        'default_urls': fields.String(required=True, description='A random string'),
        'default_redirect_uir': fields.String(required=True, description='Confidentiality'),
        'default_scopes': fields.List(required=True, description='A list of redirect urls'),
        'allowed_grant_types': fields.List(required=True, description='A list of redirect urls'),
        'allowed_response_tyoes': fields.String(required=True, description='A random string'),
        'validate_scopes': fields.String(required=True, description='Confidentiality'),
    })
'''


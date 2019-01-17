import os, logging, pyorient, time, random, json

from app.main.model.orient import OrientDB

odb = OrientDB('root', 'admin')


def create_db(db_name):
    if odb.client.db_exists(db_name):
        response_object = {
            'status': 'fail',
            'message': '%d database already exists' % db_name,
            'data': db_name
        }
        return response_object, 401
    else:
        odb.client.db_create(db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)
        logging.info("%s Database Created." % db_name)
        odb.config_pole()
        odb.demo_data()
        response_object = {
            'status': 'success',
            'message': '%d database created' % db_name,
            'data': db_name
        }
        return response_object, 200

def get_databases():
    db_list = []
    dbs = odb.client.db_list().__getattr__('databases')
    print(dbs)
    for k in dbs.keys():
        db = {'name': k, 'location': dbs[k]}
        db_list.append(db)
    response_object = {
        'status': 'success',
        'message': '%d databases found' % len(db_list),
        'data': db_list
    }
    return response_object, 200


def drop_pole():

    if odb.client.db_exists("POLE"):
        odb.client.db_drop("POLE")
        response_object = {
            'status': 'success',
            'message': 'POLE Database dropped',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'No POLE Database found',
        }
        return response_object, 500


def create_entity(r):
    open_db(r['db_name'])
    response_object = {
        'status': 'success',
        'message': '%s entity: ' % r['e_class'],
        'data': r
    }
    if r['e_class'] == 'Person':
        response_object['data']['guid'], status = odb.insert_person(FNAME=r['FNAME'], LNAME=r['LNAME'], GENDER=r['GENDER'], DOB=r['DOB'],
                                                                    POB=r['POB'], AUTH=r['AUTH'])
    elif r['e_class'] == 'Object':
        response_object['data']['guid'], status = odb.insert_object(TYPE=r['TYPE'], CATEGORY=r['CATEGORY'], DETAIL=r['DETAIL'], VAR1=r['VAR1'],
                                                                    VAR2=r['VAR2'], VAR3=r['VAR3'], AUTH=r['AUTH'])
    elif r['e_class'] == 'Location':
        response_object['data']['guid'], status = odb.insert_location(TYPE=r['TYPE'], CATEGORY=r['CATEGORY'], DETAIL=r['DETAIL'], XCOORD=r['XCOORD'],
                                                                      YCOORD=r['YCOORD'], ZCOORD=r['ZCOORD'], POSTCODE=r['POSTCODE'], AUTH=r['AUTH'])
    elif r['e_class'] == 'Event':
        response_object['data']['guid'], status = odb.insert_event(TYPE=r['TYPE'], CATEGORY=r['CATEGORY'], DETAIL=r['DETAIL'], DATE=r['DATE'],
                                                                   TIME=r['TIME'], VAR1=r['VAR1'], VAR2=r['VAR2'], VAR3=r['VAR3'], AUTH=r['AUTH'])

    else:
        response_object['status'] = 'fail'
        response_object['message'] = 'Entity class not recognized'
        return response_object, 401
    response_object['message'] = response_object['message'] + status
    return response_object, 200

def create_relationship(r):
    open_db(r['db_name'])
    response_object = {
        'status': 'success',
        'message': 'Created relation of type %s between %s and %s' % (r['r_type'], r['r_source'], r['r_target']),
        'data': odb.insert_relation(r_source=r['r_source'], r_target=r['r_target'], r_type=r['r_type'], r_var1=r['r_var1'], r_var2=r['r_var2'])
    }

    return response_object, 200


def open_pole():
    if odb.client.db_exists("POLE"):
        odb.client.db_open("POLE", odb.user, odb.pswd)
        response_object = {
            'status': 'success',
            'message': 'POLE database opened',
        }
        return response_object, 200
    else:
        logging.error("ERROR: No POLE database exists. Creating and then opening.")
        odb.create_pole()
        open_pole()
        response_object = {
            'status': 'success',
            'message': 'POLE database not detected but created and opened',
        }
        return response_object, 200


def open_db(db_name):
    if odb.client.db_exists(db_name):
        odb.client.db_open(db_name, odb.user, odb.pswd)
        response_object = {
            'status': 'success',
            'message': '%s database opened' % db_name,
        }
    else:
        response_object = {
            'status': 'error',
            'message': 'No db with name %s' % db_name,
        }
    return response_object


def update_entity(guid, updates):

    response_object = {
        'status': 'success',
        'message': 'Updating %s with %s ' % (guid, updates),
        'data': odb.update_entity(guid, updates)
    }
    return response_object


def delete_entity(guid):

    response_object = {
        'status': 'success',
        'message': 'Deleting %s ' % (guid),
        'data': odb.delete_entity(guid)
    }
    return response_object

def merge_entities(entity_a, entity_b):

    response_object = {
        'status': 'success',
        'message': 'Merging %s with %s ' % (entity_a, entity_b),
        'data': odb.merge_entities(entity_a, entity_b)
    }
    return response_object, 200

def get_search(terms):

    response_object = {
        'status': 'success',
        'message': 'Searching for entities with %s ' % (terms),
        'data': odb.get_search(terms)
    }
    return response_object, 200

def get_profile(guid):

    response_object = {
        'status': 'success',
        'message': 'Retrieved profile for ID %s ' % (guid),
        'data': odb.get_entity_profile(guid)
    }
    return response_object, 200
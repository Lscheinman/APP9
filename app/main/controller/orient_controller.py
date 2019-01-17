#!/usr/bin/env python3
# -*- coding: utf-8 -*
# /main/controller/orient_controller
from flask import request
from flask_restplus import Resource

from ..util.dto import OrientDto
from ..util.decorator import token_required
from ..service.orient_service import get_databases, open_db, create_entity, update_entity,\
                                        merge_entities, delete_entity, create_relationship, get_search, get_profile

api = OrientDto.api
_orient = OrientDto.orient
_person = OrientDto.person
_object = OrientDto.object
_location = OrientDto.location
_event = OrientDto.event
p_parser = OrientDto.p_parser
o_parser = OrientDto.o_parser
l_parser = OrientDto.l_parser
e_parser = OrientDto.e_parser
u_parser = OrientDto.u_parser
m_parser = OrientDto.m_parser
d_parser = OrientDto.d_parser
r_parser = OrientDto.r_parser
s_parser = OrientDto.s_parser
headers = ['AUTH', 'db_name', 'GUID']

@api.route('/')
@api.header('X-Header', 'Authorization')
class Orient(Resource):
    @api.doc('orient_launch')
    def get(self):
        """Get a list of POLE databases """
        return get_databases()

    @token_required
    @api.response(200, 'Database found.')
    @api.doc('Open a database')
    @api.expect(_orient, validate=True)
    @api.header('X-Collection', type=[str], collectionType='csv')
    def post(self):
        """Open a Database """
        return open_db(request.json['db_name'])

@api.route('/search')
@api.header('X-Header', 'Authorization')
class OrientSearchEntity(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Search for entities given terms')
    @api.expect(s_parser, validate=True)
    def get(self):
        """Search for an entity given terms"""
        r = request.args.to_dict()
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return get_search(r['terms'])
        else:
            return response

@api.route('/create/person')
class OrientCreatePerson(Resource):

    @token_required
    @api.expect(p_parser, validate=True)
    def post(self):
        """Create a new person class entity """
        r = request.args.to_dict()
        r['e_class'] = 'Person'
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return create_entity(r)
        else:
            return response


@api.route('/create/object')
@api.header('X-Header', 'Authorization')
class OrientCreateObject(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Create an object type entity')
    @api.expect(o_parser, validate=True)
    def post(self):
        """Create a new object class entity """
        r = request.args.to_dict()
        r['e_class'] = 'Object'
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return create_entity(r)
        else:
            return response

@api.route('/create/location')
@api.header('X-Header', 'Authorization')
class OrientCreateLocation(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Create a location type entity')
    @api.expect(l_parser, validate=True)
    def post(self):
        """Create a new location class entity """
        r = request.args.to_dict()
        r['e_class'] = 'Location'
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return create_entity(r)
        else:
            return response

@api.route('/create/event')
@api.header('X-Header', 'Authorization')
class OrientCreateEvent(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Create an event type entity')
    @api.expect(e_parser, validate=True)
    def post(self):
        """Create a new event class entity """

        r = request.args.to_dict()
        print(r)
        r['e_class'] = 'Event'
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return create_entity(r)
        else:
            return response

@api.route('/relate')
@api.header('X-Header', 'Authorization')
class OrientCreateRelationship(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Create a relationship of a certain type between a source entity (a) and a target entity (b)')
    @api.expect(r_parser, validate=True)
    def put(self):
        """Merge a source entity (a) with a target entity (b) """
        r = request.args.to_dict()
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return create_relationship(r)
        else:
            return response


@api.route('/update')
@api.header('X-Header', 'Authorization')
class OrientUpdateEntity(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Update an entity')
    @api.expect(u_parser, validate=True)
    def put(self):
        """Update an entity """
        r = request.args.to_dict()

        response = open_db(r['db_name'])
        if response['status'] == 'success':
            updates = {}
            for k in r.keys():
                if r[k] != '' and k not in headers:
                    updates[k] = r[k]
            print(updates)
            return update_entity(r['GUID'], updates)
        else:
            return response

@api.route('/merge')
@api.header('X-Header', 'Authorization')
class OrientMergeEntity(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Merge a source entity (a) with a target entity (b)')
    @api.expect(m_parser, validate=True)
    def put(self):
        """Merge a source entity (a) with a target entity (b) """
        r = request.args.to_dict()
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            updates = {}
            for k in r.keys():
                if len(r[k]) > 2 and k not in headers:
                    updates[k] = r[k]
            return merge_entities(r['entity_a'], r['entity_b'])
        else:
            return response

@api.route('/delete')
@api.header('X-Header', 'Authorization')
class OrientDeleteEntity(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Delete the entitity by ID')
    @api.expect(d_parser, validate=True)
    def delete(self):
        """Delete the entitity by ID"""
        r = request.args.to_dict()
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return delete_entity(r['GUID'])
        else:
            return response

@api.route('/profile')
@api.header('X-Header', 'Authorization')
class OrientEntityProfile(Resource):

    @token_required
    @api.header('X-Collection', type=[str], collectionType='csv')
    @api.doc('Gen an entitity based on ID')
    @api.expect(d_parser, validate=True)
    def get(self):
        """Get an entity profile based on ID"""
        r = request.args.to_dict()
        response = open_db(r['db_name'])
        if response['status'] == 'success':
            return get_profile(r['GUID'])
        else:
            return response



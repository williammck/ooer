import json
import time
from collections import OrderedDict
from hashlib import sha256
from urllib import urlencode

from flask import current_app, request, make_response
from flask_login import current_user

from .. import blueprint


@blueprint.route('/forums_auth.json')
def forums():
    client_id = current_app.config.get('FORUMS_SSO_CLIENT_ID')
    secret = current_app.config.get('FORUMS_SSO_SECRET')

    secure = True
    error = None

    if not request.args.get('client_id'):
        error = {'error': 'invalid_request', 'message': 'The client_id parameter is missing.'}
    elif request.args.get('client_id') != client_id:
        error = {'error': 'invalid_client', 'message': 'Unknown client.'}
    elif not request.args.get('timestamp') and not request.args.get('signature'):
        secure = False
    elif not request.args.get('timestamp') or not request.args.get('timestamp', u'').isnumeric():
        error = {'error': 'invalid_request', 'message': 'The timestamp parameter is missing or invalid.'}
    elif not request.args.get('signature'):
        error = {'error': 'invalid_request', 'message': 'The signature parameter is missing.'}
    elif abs(int(request.args.get('timestamp')) - time.time()) > 600:
        error = {'error': 'invalid_request', 'message': 'The timestamp parameter is invalid.'}
    else:
        signature = sha256('%s%s' % (request.args.get('timestamp'), secret)).hexdigest()
        if signature != request.args.get('signature'):
            error = {'error': 'access_denied', 'message': 'The signature parameter is invalid.'}

    if error:
        response_data = error
    elif current_user.is_authenticated:
        if secure:
            email = current_user.email
            if not email:
                email = '%s@ooer.lol' % current_user.id

            response_data = {
                'uniqueid': current_user.get_id(),
                'name': current_user.username,
                'email': email,
                'photourl': ''
            }

            query_str = urlencode(OrderedDict(sorted(response_data.items())))

            response_data['client_id'] = client_id
            response_data['signature'] = sha256('%s%s' % (query_str, secret)).hexdigest()
        else:
            response_data = {'name': current_user.username, 'photourl': ''}
    else:
        response_data = {'name': '', 'photourl': ''}

    response_json = json.dumps(response_data)

    if request.args.get('callback'):
        response = make_response('%s(%s)' % (request.args.get('callback'), response_json))
        response.mimetype = 'application/javascript'
    else:
        response = make_response(response_json)
        response.mimetype = 'application/json'

    return response

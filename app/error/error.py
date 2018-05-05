from flask import render_template, request, jsonify
from app.error import error_blueprint


@error_blueprint.app_errorhandler(403)
def forbidden(e):
    response = jsonify({'error': 'forvidden', 'status': 'fail', 'reason':str(e)})
    response.status_code = 404
    return response


@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    print(1)
    response = jsonify({'error': 'not found', 'status': 'fail', 'reason':str(e)})
    response.status_code = 404
    return response, 404


@error_blueprint.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'internal server error', 'status':'fail', 'reason':str(e)})
    response.status_code = 500
    return response

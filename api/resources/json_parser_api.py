from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource

from auth.auth import auth
from nest.json_parser import JsonParser


class Parser(Resource):
    """
    Parser API
    POST /parse?keys=args1, args2, args3
    """
    @auth.login_required
    def post(self):
        if not request.is_json or not isinstance(request.json, list):
            return 'Invalid JSON body provided', HTTPStatus.BAD_REQUEST

        keys = request.args.get('keys', [])
        if keys:
            keys = [str(item).lower().strip() for item in keys.split(',')]

        try:
            json_parser = JsonParser(request.json, keys)
            result = json_parser.parse()
            status = HTTPStatus.OK
            if not result:
                status = HTTPStatus.NO_CONTENT
        except Exception as e:
            result, status = str(e), HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            return jsonify(result).json, status

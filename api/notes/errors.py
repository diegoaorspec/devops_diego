from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def http_error(exc):
        return jsonify({"error": exc.description}), exc.code

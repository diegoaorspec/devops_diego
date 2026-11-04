import logging

from flask import Blueprint, jsonify
from pymongo.errors import PyMongoError

from notes import db

bp = Blueprint("health", __name__)
log = logging.getLogger("notes")


@bp.get("/health")
def health():
    try:
        db.get_client().admin.command("ping")
    except PyMongoError as exc:
        log.error("mongo unavailable: %s", exc)
        return jsonify({"status": "error", "mongo": "down"}), 503
    return jsonify({"status": "ok", "mongo": "up"})

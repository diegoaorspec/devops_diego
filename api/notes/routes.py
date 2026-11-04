import logging

from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, abort, current_app, jsonify, request

from notes import db
from notes.models import serialize, validate

bp = Blueprint("notes", __name__, url_prefix="/notes")
log = logging.getLogger("notes")


def _object_id(note_id):
    try:
        return ObjectId(note_id)
    except InvalidId:
        abort(400, description="invalid id")


@bp.get("")
def list_notes():
    limit = current_app.config["LIST_LIMIT"]
    docs = db.get_db().notes.find().sort("created_at", -1).limit(limit)
    return jsonify([serialize(d) for d in docs])


@bp.post("")
def create_note():
    data = request.get_json(silent=True) or {}
    note, error = validate(data, current_app.config["TITLE_MAX_LENGTH"])
    if error:
        abort(400, description=error)
    result = db.get_db().notes.insert_one(note)
    note["_id"] = result.inserted_id
    log.info("note created %s", note["_id"])
    return jsonify(serialize(note)), 201


@bp.get("/<note_id>")
def get_note(note_id):
    doc = db.get_db().notes.find_one({"_id": _object_id(note_id)})
    if doc is None:
        abort(404, description="not found")
    return jsonify(serialize(doc))


@bp.delete("/<note_id>")
def delete_note(note_id):
    result = db.get_db().notes.delete_one({"_id": _object_id(note_id)})
    if result.deleted_count == 0:
        abort(404, description="not found")
    log.info("note deleted %s", note_id)
    return "", 204

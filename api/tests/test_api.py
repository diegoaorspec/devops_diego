import mongomock
import pytest

from notes import create_app


@pytest.fixture
def client():
    app = create_app(
        {
            "LOG_FILE": None,
            "MONGO_CLIENT": mongomock.MongoClient("mongodb://localhost:27017/notes"),
        }
    )
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["mongo"] == "up"


def test_create_and_list(client):
    created = client.post("/notes", json={"title": "first", "text": "hello"})
    assert created.status_code == 201
    notes = client.get("/notes").get_json()
    assert [n["title"] for n in notes] == ["first"]


def test_title_is_required(client):
    response = client.post("/notes", json={"text": "no title"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "title is required"


def test_get_and_delete(client):
    note_id = client.post("/notes", json={"title": "to delete"}).get_json()["id"]
    assert client.get(f"/notes/{note_id}").status_code == 200
    assert client.delete(f"/notes/{note_id}").status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_invalid_id(client):
    response = client.get("/notes/not-an-id")
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid id"

from fastapi.testclient import TestClient
import pytest

from app.main import create_app


@pytest.fixture
def client():
    with TestClient(create_app("sqlite:///:memory:")) as test_client:
        yield test_client


def sample_source(**changes):
    data = {
        "title": "Learning source",
        "publisher": "Learning publisher",
        "description": "A manually added example for testing the catalogue.",
        "url": "https://example.org/learning",
        "topic": "Renewables",
        "kind": "Overview",
    }
    return data | changes


def test_filtering_combines_search_topic_and_saved_state(client):
    assert client.get("/api/health").json()["status"] == "ok"
    items = client.get("/api/sources", params={"q": "BUNDESNETZ", "topic": "Electricity"}).json()
    assert [s["publisher"] for s in items] == ["Bundesnetzagentur"]
    assert client.get("/api/sources", params={"q": "BUNDESNETZ", "topic": "Renewables"}).json() == []
    assert client.get("/api/sources", params={"q": "%"}).json() == []
    assert client.get("/api/sources", params={"saved_only": True}).json() == []
    client.patch("/api/sources/1/bookmark", json={"saved": True})
    assert [s["id"] for s in client.get("/api/sources", params={"saved_only": True}).json()] == [1]


def test_bookmark_is_idempotent_and_survives_restart(tmp_path):
    db_url = "sqlite:///" + str(tmp_path / "catalogue.db")
    with TestClient(create_app(db_url)) as first:
        for _ in range(2):
            assert first.patch("/api/sources/1/bookmark", json={"saved": True}).status_code == 200
        assert first.get("/api/overview").json()["saved"] == 1
    with TestClient(create_app(db_url)) as second:
        assert len(second.get("/api/sources").json()) == 4  # seeding is also idempotent
        assert second.get("/api/sources", params={"saved_only": True}).json()[0]["id"] == 1
        second.patch("/api/sources/1/bookmark", json={"saved": False})
        assert second.get("/api/overview").json()["saved"] == 0


def test_add_source_duplicate_and_validation(client):
    response = client.post("/api/sources", json=sample_source())
    assert response.status_code == 201
    assert response.json()["saved"] is False
    assert client.post("/api/sources", json=sample_source()).status_code == 409
    assert client.get("/api/overview").json()["sources"] == 5
    assert client.post("/api/sources", json=sample_source(url="javascript:alert(1)")).status_code == 422
    assert client.post("/api/sources", json=sample_source(title="   ")).status_code == 422
    assert client.post("/api/sources", json=sample_source(topic="Anything")).status_code == 422
    assert client.patch("/api/sources/999/bookmark", json={"saved": True}).status_code == 404
    assert client.patch("/api/sources/1/bookmark", json={"saved": "false"}).status_code == 422

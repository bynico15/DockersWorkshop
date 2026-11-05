from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "development",
        "version": "0.1.0",
    }


def test_heartbeat(client: TestClient) -> None:
    response = client.get("/api/v1/heartbeat")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

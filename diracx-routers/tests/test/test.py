from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.enabled_dependencies(["AuthSettings"])


@pytest.fixture
def test_client(client_factory):
    with client_factory.unauthenticated() as client:
        yield client


async def test_main_router_with_auth_____sub_with_auth(test_client: TestClient):
    r = test_client.get("/api/test_with_auth/auth")

    assert r.status_code == 401


async def test_main_router_with_auth_____sub_without_auth(test_client: TestClient):
    r = test_client.get("/api/test_with_auth/without-auth")

    assert r.status_code == 200


async def test_main_router_without_auth_____sub_with_auth(test_client: TestClient):
    r = test_client.get("/api/test_without_auth/auth")

    assert r.status_code == 401


async def test_main_router_without_auth_____sub_without_auth(test_client: TestClient):
    r = test_client.get("/api/test_without_auth/without-auth")

    assert r.status_code == 200

"""Shared test fixtures.

``client`` gives you a FastAPI test client backed by a throwaway database, so tests
never depend on each other's writes.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app import db as db_module
from app import model_client as mc
from app.main import app
from app.routes import summary as summary_route


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db_module, "DB_PATH", tmp_path / "test.db")
    db_module.reset(tmp_path / "test.db")
    mc.reset_client()
    summary_route.clear_cache()
    with TestClient(app) as c:
        yield c
    db_module.reset(tmp_path / "test.db")
    mc.reset_client()
    summary_route.clear_cache()


@pytest.fixture()
def stub():
    """A well-behaved stub client. Override fields to make it misbehave."""
    return mc.StubModelClient()

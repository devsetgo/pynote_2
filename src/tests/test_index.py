# -*- coding: utf-8 -*-
import unittest
import uuid

from async_asgi_testclient import TestClient

from main import app

# from starlette.testclient import TestClient


class Test(unittest.TestCase):
    async def test_index(self):

        client = await TestClient(app)
        url = f"/"
        response = client.get(url)
        assert response.status_code == 200

    async def test_health_pages(self):

        client = await TestClient(app)
        url = f"/health"
        response = client.get(url)
        assert response.status_code == 200

    async def test_index__error(self):

        url = f"/{uuid.uuid1()}.html"
        client = await TestClient(app)
        response = client.get(url)
        assert response.status_code == 404

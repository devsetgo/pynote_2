# -*- coding: utf-8 -*-
import unittest
import uuid

from async_asgi_testclient import TestClient

from main import app

# from starlette.testclient import TestClient
base_url: str = "/dashboard"


class Test(unittest.TestCase):
    async def test_dash(self):

        client = await TestClient(app)
        url = f"{base_url}/"
        response = client.get(url)
        assert response.status_code == 200

    # async def test_new(self):

    #     client = await TestClient(app)
    #     url = f"{base_url}/new"
    #     response = client.get(url)
    #     assert response.status_code == 200

    async def test_dash_error(self):

        url = f"{base_url}/{uuid.uuid1()}.html"
        client = await TestClient(app)
        response = client.get(url)
        assert response.status_code == 404

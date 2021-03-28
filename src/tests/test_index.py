# -*- coding: utf-8 -*-
import unittest
import uuid

from starlette.testclient import TestClient

from main import app
from settings import config_settings

# from async_asgi_testclient import TestClient


# def test_index():
#     client = TestClient(app)
#     url = f"/"
#     response = client.get(url)
#     assert response.status_code == 303


# def test_login():
#     client = TestClient(app)
#     data = {
#         "user": config_settings.admin_user_name,
#         "password": config_settings.admin_user_key,
#     }
#     url = f"/user/login"
#     response = client.post(url, data=data)
#     assert response.status_code == 303


# def test_health_pages():
#     client = TestClient(app)
#     url = f"/health"
#     response = client.get(url)
#     assert response.status_code == 200


# def test_index_error():
#     url = f"/{uuid.uuid1()}.html"
#     client = TestClient(app)
#     response = client.get(url)
#     assert response.status_code == 404

client = TestClient(app)


class Test(unittest.TestCase):
    def test_index(self):
        # client = TestClient(app)
        url = f"/"
        response = client.get(url)
        assert response.status_code == 303

    def test_login(self):
        # client = TestClient(app)
        data = {
            "user": config_settings.admin_user_name,
            "password": config_settings.admin_user_key,
        }
        url = f"/user/login"
        response = client.post(url, data=data)
        assert response.status_code == 303

    def test_health_pages(self):
        # client = TestClient(app)
        url = f"/health"
        response = client.get(url)
        assert response.status_code == 200

    def test_index_error(self):
        url = f"/{uuid.uuid1()}.html"
        # client = TestClient(app)
        response = client.get(url)
        assert response.status_code == 303

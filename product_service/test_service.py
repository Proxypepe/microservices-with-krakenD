import unittest
from mongoengine import connect, disconnect
import httpx
import pytest
from main import app
from httpx import AsyncClient


class TestEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    async def test_get_all(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resource = await ac.get('/v1/products')
            assert resource.status_code == 201



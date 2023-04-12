import os
import pytest
import requests

import libsql_client

@pytest.fixture
def http_url():
    return os.getenv("HTTP_URL", "http://localhost:8080")

@pytest.fixture
def ws_url():
    return os.getenv("WS_URL", "ws://localhost:8080")

@pytest.fixture
def file_url(tmp_path):
    return f"file://{tmp_path.absolute() / 'test.db'}"

def _url(request):
    if request.param == "http":
        return request.getfixturevalue("http_url")
    elif request.param == "ws":
        return request.getfixturevalue("ws_url")
    elif request.param == "file":
        return request.getfixturevalue("file_url")
    else:
        assert False, f"Bad URL request.param: {request.param!r}"

#@pytest.fixture(params=["http", "ws", "file"])
@pytest.fixture(params=["file"])
def url(request):
    return _url(request)

#@pytest.fixture(params=["ws", "file"])
@pytest.fixture(params=["file"])
def transaction_url(request):
    return _url(request)

@pytest.fixture
def client(url):
    with libsql_client.create_client(url) as c:
        yield c

@pytest.fixture
def transaction_client(transaction_url):
    with libsql_client.create_client(transaction_url) as c:
        yield c

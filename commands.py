from sanic.server import HttpProtocol

from service_api.application import app
from service_api.constants import get_port


def runserver():
    class CGDPHttpProtocol(HttpProtocol):

        def __init__(self, *args, **kwargs):
            if "request_timeout" in kwargs:
                kwargs.pop("request_timeout")
            super().__init__(*args, request_timeout=300, **kwargs)

    app.run(protocol=CGDPHttpProtocol, port = get_port(app.name))

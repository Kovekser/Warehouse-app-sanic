from sanic.app import Sanic

from service_api.resources.smokeview import SmokeResource


def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")
    app.go_fast(debug=True)
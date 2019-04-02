from sanic.app import Sanic

from service_api.resources import SmokeView


def create_app():
    app = Sanic()
    app.add_route(SmokeView.as_view(), "/smoke")
    app.go_fast(debug=True)
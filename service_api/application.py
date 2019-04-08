from sanic.app import Sanic

from service_api.resources.smokeview import SmokeResource
from service_api.resources.client_resource import ClientAllResource
from service_api.resources.parseltype_resource import ParselTypeAllResource
from service_api.resources.storage_resource import StorageAllResource
from service_api.resources.parsel_resource import ParselAllResource
from service_api.resources.supply_resource import SupplyAllResource


def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")
    app.add_route(ClientAllResource().as_view(), "/client")
    app.add_route(ParselTypeAllResource().as_view(), "/parseltype")
    app.add_route(StorageAllResource().as_view(), "/storage")
    app.add_route(ParselAllResource().as_view(), "/parsel")
    app.add_route(SupplyAllResource().as_view(), "/supply")
    return app


app = create_app()

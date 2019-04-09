from sanic.app import Sanic

from service_api.resources.smokeview import SmokeResource
from service_api.resources.client_resource import ClientAllResource, ClientResource
from service_api.resources.parseltype_resource import ParselTypeAllResource, ParselTypeResource
from service_api.resources.storage_resource import StorageAllResource, StorageResource
from service_api.resources.parsel_resource import ParselAllResource, ParselResource
from service_api.resources.supply_resource import SupplyAllResource, SupplyResource


def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")
    app.add_route(ClientAllResource().as_view(), "/client")
    app.add_route(ClientResource().as_view(), "/client/<client_id>")
    app.add_route(ParselTypeAllResource().as_view(), "/parseltype")
    app.add_route(ParselTypeResource().as_view(), "/parseltype/<type_id>")
    app.add_route(StorageAllResource().as_view(), "/storage")
    app.add_route(StorageResource().as_view(), "/storage/<storage_id>")
    app.add_route(ParselAllResource().as_view(), "/parsel")
    app.add_route(ParselResource().as_view(), "/parsel/<parsel_id>")
    app.add_route(SupplyAllResource().as_view(), "/supply")
    app.add_route(SupplyResource().as_view(), "/supply/<supply_id>")
    return app


app = create_app()

from sanic.app import Sanic

from service_api.resources.smoke_resource import SmokeResource
from service_api.resources.client_resource import ClientAllResource, ClientResource
from service_api.resources.parceltype_resource import ParcelTypeAllResource, ParcelTypeResource
from service_api.resources.storage_resource import StorageAllResource, StorageResource
from service_api.resources.parcel_resource import ParcelAllResource, ParcelResource, ParcelQueryResource
from service_api.resources.supply_resource import SupplyAllResource, SupplyResource


def create_app():
    app = Sanic()
    app.add_route(SmokeResource.as_view(), "/smoke")

    app.add_route(ClientAllResource().as_view(), "/client")
    app.add_route(ClientResource().as_view(), "/client/<client_id>")

    app.add_route(ParcelTypeAllResource().as_view(), "/parceltype")
    app.add_route(ParcelTypeResource().as_view(), "/parceltype/<type_id>")

    app.add_route(StorageAllResource().as_view(), "/storage")
    app.add_route(StorageResource().as_view(), "/storage/<storage_id>")

    app.add_route(ParcelAllResource().as_view(), "/parcel")
    app.add_route(ParcelResource().as_view(), "/parcel/<parcel_id>")
    app.add_route(ParcelQueryResource().as_view(), "/parcel/<parcel_type>/<storage_id>")

    app.add_route(SupplyAllResource().as_view(), "/supply")
    app.add_route(SupplyResource().as_view(), "/supply/<supply_id>")
    return app


app = create_app()

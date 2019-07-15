from sanic.app import Sanic
from sanic.blueprints import Blueprint

from service_api.constants import DEFAULT_SERVICE_NAME
from service_api.resources.smoke_resource import SmokeResource
from service_api.resources.client_resource import ClientAllResource, ClientResource
from service_api.resources.parceltype_resource import ParcelTypeAllResource, ParcelTypeResource
from service_api.resources.storage_resource import StorageAllResource, StorageResource
from service_api.resources.parcel_resource import (ParcelAllResource,
                                                   ParcelResource,
                                                   ParcelQueryResource,
                                                   ParcelReportResource,)
from service_api.resources.supply_resource import SupplyAllResource, SupplyResource


def create_app():
    app = Sanic(DEFAULT_SERVICE_NAME)
    api_prefix = f'/{DEFAULT_SERVICE_NAME}'
    api = Blueprint('warehouse', url_prefix=api_prefix)
    api.add_route(SmokeResource.as_view(), "/smoke")

    api.add_route(ClientAllResource().as_view(), "/client")
    api.add_route(ClientResource().as_view(), "/client/<client_id>")

    api.add_route(ParcelTypeAllResource().as_view(), "/parceltype")
    api.add_route(ParcelTypeResource().as_view(), "/parceltype/<type_id>")

    api.add_route(StorageAllResource().as_view(), "/storage")
    api.add_route(StorageResource().as_view(), "/storage/<storage_id>")

    api.add_route(ParcelAllResource().as_view(), "/parcel")
    api.add_route(ParcelResource().as_view(), "/parcel/<parcel_id>")
    api.add_route(ParcelQueryResource().as_view(), "/parcel/<parcel_type>/<storage_id>")
    api.add_route(ParcelReportResource().as_view(), "/parcel/report")

    api.add_route(SupplyAllResource().as_view(), "/supply")
    api.add_route(SupplyResource().as_view(), "/supply/<supply_id>")
    app.blueprint(api)
    return app


app = create_app()

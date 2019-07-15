
from service_api.utils.rest_client.base import RESTClientRegistry
from service_api.utils.rest_client.reports import ReportsRESTClient


__all__ = ("RESTClientRegistry",)


RESTClientRegistry.register('reports', ReportsRESTClient)

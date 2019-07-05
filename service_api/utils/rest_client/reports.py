from service_api.utils.rest_client.base import ServiceDiscovery
from service_api.utils.rest_client.base import BaseRESTClient


class ReportsRESTClient(BaseRESTClient):
    service_config = ServiceDiscovery.reports_api

    async def generate_report(self, url_path, json_data):
        return await self.get('POST', url_path, json_data)

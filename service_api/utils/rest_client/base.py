import aiohttp
from collections import namedtuple
from service_api.constants import get_port


ServiceConfiguration = namedtuple("ServiceConfiguration", ["service_path", "url_format"])

class ServiceDiscovery:
    reports_api = ServiceConfiguration('whreports', f"http://localhost:{get_port('whreports')}/whreports")


class RESTClientRegistry:
    _clients = {}

    @classmethod
    def register(cls, name, rest_cls):
        cls._clients[name] = rest_cls

    @classmethod
    def get(cls, name):
        return cls._clients.get(name)


class BaseRESTClient:
    service_config = None

    async def get(self, request_method, url_path, input_data):
        data, status_code = await self.make_http_request(request_method, url=url_path, input_data=input_data)
        return data, status_code

    async def make_http_request(self, request_method, url, input_data):
        service_base_url = self.service_config.url_format
        request_url = f"{service_base_url}/{url}"
        print(request_url)
        async with aiohttp.ClientSession() as session:
            async with session.request(method=request_method, url=request_url, json=input_data) as response:
                response_json = await response.json()
                return response_json, response.status

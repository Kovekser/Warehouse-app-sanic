from sanic.views import HTTPMethodView
from sanic.response import json
import pprint

from service_api.domain.clients import get_all_clients, insert_one


class ClientAllResource(HTTPMethodView):
    async def get(self, request):
        a = await get_all_clients()
        for row in a:
            row['id'] = str(row['id'])

        return json({"Clients": a})

    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created user'})
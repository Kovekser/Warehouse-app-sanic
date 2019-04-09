from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.clients import get_all_clients, insert_one_client, get_client_by_id


class ClientAllResource(HTTPMethodView):
    async def get(self, request):
        all_clients = await get_all_clients()
        for row in all_clients:
            row['id'] = str(row['id'])

        return json({"Clients": all_clients})

    async def post(self, request):
        await insert_one_client(request.json)
        return json({'msg': 'Successfully created user'})

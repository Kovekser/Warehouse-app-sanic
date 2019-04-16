from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.clients import (get_all_clients,
                                        insert_one_client,
                                        get_client_by_id,
                                        delete_one_client,
                                        update_client_by_id)


class ClientAllResource(HTTPMethodView):
    async def get(self, request):
        all_clients = await get_all_clients()
        for row in all_clients:
            row['id'] = str(row['id'])
        return json({"Clients": all_clients})

    async def post(self, request):
        await insert_one_client(request.json)
        return json({'msg': 'Successfully created user'})


class ClientResource(HTTPMethodView):
    async def get(self, request, client_id):
        client = await get_client_by_id(client_id)
        if not client:
            return json({'msg': 'Client with id {} does not exist'.format(client_id)})
        client['id'] = str(client['id'])
        return json({"Client": client})

    async def delete(self, request, client_id):
        client = await get_client_by_id(client_id)
        await delete_one_client(client_id)
        return json({'msg': 'Successfully deleted user {}'.format(client['email'])})

    async def put(self, request, client_id):
        client = await get_client_by_id(client_id)
        await update_client_by_id(client_id, request.json)
        return json({'msg': 'User {} successfully updated'.format(client['email'])})

from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.clients import (get_all_clients,
                                        insert_one_client,
                                        get_client_by_id,
                                        delete_one_client,
                                        update_client_by_id)
from service_api.forms import ClientSchema
from service_api.utils.response_utils import map_response


class ClientAllResource(HTTPMethodView):
    async def get(self, request):
        all_clients = await get_all_clients()
        return json({"Clients": map_response(all_clients)})

    async def post(self, request):
        json_input = request.json
        for client in json_input:
            client_data, err = ClientSchema().load(client)
            if err:
                return json({'Errors': err}, status=404)

            await insert_one_client(client_data)
        return json({'msg': 'Successfully created user'})


class ClientResource(HTTPMethodView):
    async def get(self, request, client_id):
        _, err = ClientSchema().dump({'id': client_id})
        if err:
            return json({'Errors': err}, status=404)

        client = await get_client_by_id(client_id)
        if client:
            return json({"Client": map_response(client)})
        return json({'msg': 'Client with id {} does not exist'.format(client_id)}, status=404)

    async def delete(self, request, client_id):
        _, err = ClientSchema().dump({'id': client_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_client(client_id)
        if result:
            return json({'msg': 'Successfully deleted user {}'.format(result[0]['email'])})
        return json({'msg': 'User with id {} does not exist'.format(client_id)}, status=404)

    async def put(self, request, client_id):
        json_input = request.json
        json_input['id'] = str(client_id)
        client_data, err = ClientSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        result = await update_client_by_id(client_data)
        if result:
            return json({'msg': 'User {} successfully updated'.format(result[0]['email'])})
        return json({'msg': 'User with id {} does not exist'.format(client_id)}, status=404)

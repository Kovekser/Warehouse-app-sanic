import uuid

from sanic.views import HTTPMethodView
from sanic.response import json
from service_api.domain.supply import (get_all_supply,
                                       insert_one_supply,
                                       get_supply_by_id,
                                       delete_one_supply,
                                       update_supply_by_id)
from service_api.forms import SupplySchema
from service_api.utils.response_utils import map_response


class SupplyAllResource(HTTPMethodView):
    async def get(self, request):
        all_supply = await get_all_supply()
        return json({"Supply": map_response(all_supply)})

    async def post(self, request):
        json_input = request.json
        supply_data, err = SupplySchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        await insert_one_supply(supply_data)
        return json({'msg': 'Successfully created supply'})


class SupplyResource(HTTPMethodView):
    async def get(self, request, supply_id):
        _, err = SupplySchema().dump({'id': supply_id})
        if err:
            return json({'Errors': err}, status=404)

        supply = await get_supply_by_id(supply_id)
        if supply:
            return json({"Supply": map_response(supply)})
        return json({'msg': 'Supply with id {} does not exist'.format(supply_id)}, status=404)


    async def delete(self, request, supply_id):
        _, err = SupplySchema().dump({'id': supply_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_supply(supply_id)
        if result:
            return json({'msg': 'Successfully deleted supply {}'.format(result[0]['id'])})
        return json({'msg': 'Supply with id {} does not exist'.format(supply_id)}, status=404)

    async def put(self, request, supply_id):
        json_input = request.json
        json_input['id'] = supply_id
        supply_data, err = SupplySchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        result = await update_supply_by_id(supply_data)
        if result:
            return json({'msg': 'Supply {} successfully updated'.format(result[0]['id'])})
        return json({'msg': 'Supply with id {} does not exist'.format(supply_id)}, status=404)

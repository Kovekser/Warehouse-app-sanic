from sanic.views import HTTPMethodView
from sanic.response import json
import uuid


from service_api.domain.supply import (get_all_supply,
                                       insert_one_supply,
                                       get_supply_by_id,
                                       delete_one_supply,
                                       update_supply_by_id)


class SupplyAllResource(HTTPMethodView):
    async def get(self, request):
        all_supply = await get_all_supply()
        for row in all_supply:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])
        return json({"Supply": all_supply})

    async def post(self, request):
        await insert_one_supply(request.json)
        return json({'msg': 'Successfully created supply'})


class SupplyResource(HTTPMethodView):
    async def get(self, request, supply_id):
        supply = await get_supply_by_id(supply_id)
        for k in supply:
            if isinstance(supply[k], uuid.UUID):
                supply[k] = str(supply[k])
        return json({"Supply": supply})

    async def delete(self, request, supply_id):
        await delete_one_supply(supply_id)
        return json({'msg': 'Successfully deleted supply'})

    async def put(self, request, supply_id):
        await update_supply_by_id(supply_id, request.json)
        return json({'msg': 'Supply {} succesfully updated'.format(supply_id)})

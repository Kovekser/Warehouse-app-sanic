from sanic.views import HTTPMethodView
from sanic.response import json
import uuid


from service_api.domain.supply import get_all_supply, insert_one


class SupplyAllResource(HTTPMethodView):
    async def get(self, request):
        all_supply = await get_all_supply()
        for row in all_supply:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])
        return json({"Supply": all_supply})

    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created supply'})

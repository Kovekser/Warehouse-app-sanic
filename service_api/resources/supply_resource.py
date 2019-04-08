from sanic.views import HTTPMethodView
from sanic.response import json
import uuid


from service_api.domain.supply import get_all_supply, insert_one


class SupplyAllResource(HTTPMethodView):
    async def get(self, request):
        a = await get_all_supply()
        for row in a:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])
        return json({"Supply": a})

    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created supply'})

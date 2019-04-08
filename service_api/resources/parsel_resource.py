import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel import get_all_parsels, insert_one


class ParselAllResource(HTTPMethodView):
    async def get(self, request):
        a = await get_all_parsels()
        for row in a:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])

        return json({"Parsels": a})

    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created parsel'})
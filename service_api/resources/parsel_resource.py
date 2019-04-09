import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel import get_all_parsels, insert_one_parsel


class ParselAllResource(HTTPMethodView):
    async def get(self, request):
        all_parsel = await get_all_parsels()
        for row in all_parsel:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])

        return json({"Parsels": all_parsel})


    async def post(self, request):
        await insert_one_parsel(request.json)
        return json({'msg': 'Successfully created parsel'})

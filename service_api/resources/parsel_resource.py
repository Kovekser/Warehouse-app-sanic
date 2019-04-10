import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel import (get_all_parsels,
                                       insert_one_parsel,
                                       get_parsel_by_id,
                                       delete_one_parsel,
                                       update_parsel_by_id)


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


class ParselResource(HTTPMethodView):
    async def get(self, request, parsel_id):
        parsel = await get_parsel_by_id(parsel_id)
        for k in parsel:
            if isinstance(parsel[k], uuid.UUID):
                parsel[k] = str(parsel[k])
        return json({"Parsel": parsel})

    async def delete(self, request, parsel_id):
        await delete_one_parsel(parsel_id)
        return json({'msg': 'Successfully deleted parsel'})

    async def put(self, request, parsel_id):
        await update_parsel_by_id(parsel_id, request.json)
        return json({'msg': 'Parsel {} succesfully updated'.format(parsel_id)})

from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel_type import get_all_types, insert_one_type, get_type_by_id


class ParselTypeAllResource(HTTPMethodView):
    async def get(self, request):
        all_types = await get_all_types()
        for row in all_types:
            row['id'] = str(row['id'])
        return json({"Types": all_types})

    async def post(self, request):
        await insert_one_type(request.json)
        return json({'msg': 'Successfully created parsel type'})


class ParselTypeResource(HTTPMethodView):
    async def get(self, request, type_id):
        pars_type = await get_type_by_id(type_id)
        pars_type['id'] = str(pars_type['id'])
        return json({"Parsel_type": pars_type})

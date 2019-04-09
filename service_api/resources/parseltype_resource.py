from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel_type import get_all_types, insert_one_type


class ParselTypeAllResource(HTTPMethodView):
    async def get(self, request):
        all_types = await get_all_types()
        for row in all_types:
            row['id'] = str(row['id'])

        return json({"Types": all_types})


    async def post(self, request):
        await insert_one_type(request.json)
        return json({'msg': 'Successfully created parsel type'})

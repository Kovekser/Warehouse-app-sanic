from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel_type import get_all_types, insert_one


class ParselTypeAllResource(HTTPMethodView):
    async def get(self, request):
        a = await get_all_types()
        for row in a:
            row['id'] = str(row['id'])

        return json({"Types": a})


    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created parsel type'})

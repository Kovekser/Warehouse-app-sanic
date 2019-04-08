from sanic.views import HTTPMethodView
from sanic.response import json
import pprint

from service_api.domain.storage import get_all_storage, insert_one


class StorageAllResource(HTTPMethodView):
    async def get(self, request):
        a = await get_all_storage()
        for row in a:
            row['id'] = str(row['id'])

        return json({"Storages": a})

    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created storage'})
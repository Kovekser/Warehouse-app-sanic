from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.storage import get_all_storage, insert_one


class StorageAllResource(HTTPMethodView):
    async def get(self, request):
        all_storage = await get_all_storage()
        for row in all_storage:
            row['id'] = str(row['id'])

        return json({"Storages": all_storage})


    async def post(self, request):
        await insert_one(request.json)
        return json({'msg': 'Successfully created storage'})

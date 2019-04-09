from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.storage import get_all_storage, insert_one_storage, get_storage_by_id


class StorageAllResource(HTTPMethodView):
    async def get(self, request):
        all_storage = await get_all_storage()
        for row in all_storage:
            row['id'] = str(row['id'])

        return json({"Storages": all_storage})


    async def post(self, request):
        await insert_one_storage(request.json)
        return json({'msg': 'Successfully created storage'})


class StorageResource(HTTPMethodView):
    async def get(self, request, storage_id):
        storage = await get_storage_by_id(storage_id)
        storage['id'] = str(storage['id'])
        return json({"Storage": storage})

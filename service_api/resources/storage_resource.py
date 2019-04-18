from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.storage import (get_all_storage,
                                        insert_one_storage,
                                        get_storage_by_id,
                                        delete_one_storage,
                                        update_storage_by_id)
from service_api.resources.forms import StorageSchema


class StorageAllResource(HTTPMethodView):
    async def get(self, request):
        all_storage = await get_all_storage()
        for row in all_storage:
            row['id'] = str(row['id'])
        return json({"Storages": all_storage})

    async def post(self, request):
        json_input = request.json
        storage_data, err = StorageSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        await insert_one_storage(storage_data)
        return json({'msg': 'Successfully created storage'})


class StorageResource(HTTPMethodView):
    async def get(self, request, storage_id):
        storage_data, err = StorageSchema().dump({'id': storage_id})
        if err:
            return json({'Errors': err}, status=404)

        storage = await get_storage_by_id(storage_id)
        if storage:
            storage['id'] = str(storage['id'])
            return json({"Storage": storage})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)}, status=404)

    async def delete(self, request, storage_id):
        storage_data, err = StorageSchema().dump({'id': storage_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_storage(storage_id)
        if result:
            return json({'msg': 'Successfully deleted storage {}'.format(result['address'])})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)}, status=404)

    async def put(self, request, storage_id):
        json_input = request.json
        json_input['id'] = storage_id
        storage_data, err = StorageSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        storage = await update_storage_by_id(json_input)
        if storage:
            return json({'msg': 'Storage {} successfully updated'.format(storage['address'])})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)},status=404)

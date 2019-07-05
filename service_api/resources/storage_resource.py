from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.storage import (get_all_storage,
                                        insert_one_storage,
                                        get_storage_by_id,
                                        delete_one_storage,
                                        update_storage_by_id)
from service_api.forms import StorageSchema
from service_api.utils.response_utils import map_response


class StorageAllResource(HTTPMethodView):
    async def get(self, request):
        all_storage, _ = await get_all_storage()
        return json({"Storages": map_response(all_storage)})

    async def post(self, request):
        json_input = request.json
        storage_data, err = StorageSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        await insert_one_storage(storage_data)
        return json({'msg': 'Successfully created storage'})


class StorageResource(HTTPMethodView):
    async def get(self, request, storage_id):
        _, err = StorageSchema().dump({'id': storage_id})
        if err:
            return json({'Errors': err}, status=404)

        storage, _ = await get_storage_by_id(storage_id)
        if storage:
            return json({"Storage": map_response(storage)})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)}, status=404)

    async def delete(self, request, storage_id):
        _, err = StorageSchema().dump({'id': storage_id})
        if err:
            return json({'Errors': err}, status=404)

        result, _ = await delete_one_storage(storage_id)
        if result:
            return json({'msg': 'Successfully deleted storage {}'.format(result[0]['address'])})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)}, status=404)

    async def put(self, request, storage_id):
        json_input = request.json
        json_input['id'] = storage_id
        storage_data, err = StorageSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        storage, _ = await update_storage_by_id(storage_data)
        if storage:
            return json({'msg': 'Storage {} successfully updated'.format(storage[0]['address'])})
        return json({'msg': 'Storage with id {} does not exist'.format(storage_id)},status=404)

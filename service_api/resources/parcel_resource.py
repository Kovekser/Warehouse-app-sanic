import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parcel import (get_all_parcels,
                                       insert_one_parcel,
                                       get_parcel_by_id,
                                       delete_one_parcel,
                                       update_parcel_by_id)
from service_api.forms import ParcelSchema


class ParcelAllResource(HTTPMethodView):
    async def get(self, request):
        all_parcel = await get_all_parcels()
        for row in all_parcel:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])
        return json({"Parcels": all_parcel})

    async def post(self, request):
        json_input = request.json
        parcel_data, err = ParcelSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        await insert_one_parcel(parcel_data)
        return json({'msg': 'Successfully created parcel'})


class ParcelResource(HTTPMethodView):
    async def get(self, request, parcel_id):
        _, err = ParcelSchema().dump({'id': parcel_id})
        if err:
            return json({'Errors': err}, status=404)

        parcel = await get_parcel_by_id(parcel_id)
        if parcel:
            for k in parcel:
                if isinstance(parcel[k], uuid.UUID):
                    parcel[k] = str(parcel[k])
            return json({"Parcel": parcel})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)

    async def delete(self, request, parcel_id):
        _, err = ParcelSchema().dump({'id': parcel_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_parcel(parcel_id)
        if result:
            return json({'msg': 'Successfully deleted parcel {}'.format(result['id'])})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)

    async def put(self, request, parcel_id):
        json_input = request.json
        json_input['id'] = parcel_id
        parcel_data, err = ParcelSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        result = await update_parcel_by_id(parcel_data)
        if result:
            return json({'msg': 'Parcel {} successfully updated'.format(result['id'])})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)

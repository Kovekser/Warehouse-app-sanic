import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parcel import (get_all_parcels,
                                       insert_one_parcel,
                                       get_parcel_by_id,
                                       delete_one_parcel,
                                       update_parcel_by_id)


class ParcelAllResource(HTTPMethodView):
    async def get(self, request):
        all_parcel = await get_all_parcels()
        for row in all_parcel:
            for k in row:
                if isinstance(row[k], uuid.UUID):
                    row[k] = str(row[k])
        return json({"Parcels": all_parcel})

    async def post(self, request):
        await insert_one_parcel(request.json)
        return json({'msg': 'Successfully created parcel'})


class ParcelResource(HTTPMethodView):
    async def get(self, request, parcel_id):
        parcel = await get_parcel_by_id(parcel_id)
        if not parcel:
            return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)})
        for k in parcel:
            if isinstance(parcel[k], uuid.UUID):
                parcel[k] = str(parcel[k])
        return json({"Parcel": parcel})

    async def delete(self, request, parcel_id):
        await delete_one_parcel(parcel_id)
        return json({'msg': 'Successfully deleted parcel'})

    async def put(self, request, parcel_id):
        await update_parcel_by_id(parcel_id, request.json)
        return json({'msg': 'Parcel {} successfully updated'.format(parcel_id)})

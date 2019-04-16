from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel_type import (get_all_types,
                                            insert_one_type,
                                            get_type_by_id,
                                            delete_one_type,
                                            update_type_by_id)


class ParcelTypeAllResource(HTTPMethodView):
    async def get(self, request):
        all_types = await get_all_types()
        for row in all_types:
            row['id'] = str(row['id'])
        return json({"Types": all_types})

    async def post(self, request):
        await insert_one_type(request.json)
        return json({'msg': 'Successfully created parcel type'})


class ParcelTypeResource(HTTPMethodView):
    async def get(self, request, type_id):
        pars_type = await get_type_by_id(type_id)
        if not pars_type:
            return json({'msg': 'Parcel type with id {} does not exist'.format(type_id)})
        pars_type['id'] = str(pars_type['id'])
        return json({"Parcel_type": pars_type})

    async def delete(self, request, type_id):
        pars_type = await get_type_by_id(type_id)
        await delete_one_type(type_id)
        return json({'msg': 'Successfully deleted parcel type {}'.format(pars_type['type_name'])})

    async def put(self, request, type_id):
        pars_type = await get_type_by_id(type_id)
        await update_type_by_id(type_id, request.json)
        return json({'msg': 'Parcel type {} successfully updated'.format(pars_type['type_name'])})

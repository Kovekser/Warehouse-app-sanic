from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parsel_type import (get_all_types,
                                            insert_one_type,
                                            get_type_by_id,
                                            delete_one_type,
                                            update_type_by_id)
from service_api.resources.forms import ParceltypeSchema


class ParcelTypeAllResource(HTTPMethodView):
    async def get(self, request):
        all_types = await get_all_types()
        for row in all_types:
            row['id'] = str(row['id'])
        return json({"Types": all_types})

    async def post(self, request):
        json_input = request.json
        type_data, err = ParceltypeSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)
        await insert_one_type(type_data)
        return json({'msg': 'Successfully created parcel type'})


class ParcelTypeResource(HTTPMethodView):
    async def get(self, request, type_id):
        type_data, err = ParceltypeSchema().dump({'id': type_id})
        if err:
            return json({'Errors': err}, status=404)

        pars_type = await get_type_by_id(type_id)
        if pars_type:
            pars_type['id'] = str(pars_type['id'])
            return json({"Parcel_type": pars_type})
        return json({'msg': 'Parcel type with id {} does not exist'.format(type_id)}, status=404)


    async def delete(self, request, type_id):
        type_data, err = ParceltypeSchema().dump({'id': type_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_type(type_id)
        if result:
            return json({'msg': 'Successfully deleted parcel type {}'.format(result['type_name'])})
        return json({'msg': 'Parcel type with id {} does not exist'.format(type_id)}, status=404)

    async def put(self, request, type_id):
        json_input = request.json
        json_input['id'] = type_id
        type_data, err = ParceltypeSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        result = await update_type_by_id(type_data)
        if result:
            return json({'msg': 'Parcel type {} successfully updated'.format(result['type_name'])})
        return json({'msg': 'Parcel type with id {} does not exist'.format(type_id)}, status=404)

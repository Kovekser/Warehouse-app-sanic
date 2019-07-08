import uuid
from sanic.views import HTTPMethodView
from sanic.response import json


from service_api.domain.parcel import (get_all_parcels,
                                       insert_one_parcel,
                                       get_parcel_by_id,
                                       delete_one_parcel,
                                       update_parcel_by_id,
                                       get_parcel_by_type_and_storage)
from service_api.forms import ParcelSchema
from service_api.utils.rest_client.base import RESTClientRegistry
from service_api.utils.response_utils import map_response


class ParcelAllResource(HTTPMethodView):
    async def get(self, request):
        all_parcel = await get_all_parcels()
        return json({"Parcels": map_response(all_parcel)})

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
            return json({"Parcel": map_response(parcel)})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)

    async def delete(self, request, parcel_id):
        _, err = ParcelSchema().dump({'id': parcel_id})
        if err:
            return json({'Errors': err}, status=404)

        result = await delete_one_parcel(parcel_id)
        if result:
            return json({'msg': 'Successfully deleted parcel {}'.format(result[0]['id'])})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)

    async def put(self, request, parcel_id):
        json_input = request.json
        json_input['id'] = parcel_id
        parcel_data, err = ParcelSchema().load(json_input)
        if err:
            return json({'Errors': err}, status=404)

        result = await update_parcel_by_id(parcel_data)
        if result:
            return json({'msg': 'Parcel {} successfully updated'.format(result[0]['id'])})
        return json({'msg': 'Parcel with id {} does not exist'.format(parcel_id)}, status=404)


class ParcelQueryResource(HTTPMethodView):
    async def get(self, request, parcel_type, storage_id):
        """ Select parcels from database with pre-defined parameters:
        param parcel_type (str): name of parcel type
        param storage_id (str): UUID of storage received the parcel
        param request: request.json:
        "date" (optional) is date of request. Can be: empty - returns all parcels, single - returns parcels for one day,
                                    date range - returns parcels for the period
        return: list of parcels (if there are more than 1 parcels otherwise dict) and total cost of parcels.
        """
        _, err = ParcelSchema().dump({'id': storage_id})
        if err:
            return json({'Errors': err}, status=404)
        date = request.args.get('date', None)

        parcels = await get_parcel_by_type_and_storage(parcel_type, storage_id, date)
        if parcels:
            total_cost = sum(i['cost'] for i in parcels)\
                # if isinstance(parcels, list) else parcels['cost']

            return json({'parcels': map_response(parcels), 'total_cost': total_cost}, status=200)
        return json({'parcels': parcels, 'total_cost': 0}, status=200)


class ParcelReportResource(HTTPMethodView):
    async def post(self, request):
        reports_client = RESTClientRegistry.get('reports')
        report_data = await get_parcel_by_type_and_storage(request.json.get('parcel_type'),
                                                                 request.json.get('storage_id'),
                                                                 request.json.get('date', None))
        head = list(report_data[0].keys())

        response, status_code = await reports_client().generate_report(url_path='report', json_data={'report_type': 'parcels',
                                                                                 'headers': head,
                                                                                 'data': map_response(report_data)})
        print(response, status_code)
        return json({'result': response}, status=status_code)

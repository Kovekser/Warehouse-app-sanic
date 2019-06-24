import decimal
import datetime
import uuid
import calendar
import collections

def map_response(raw_response):
    def prepare_for_json(o):
        if isinstance(o, decimal.Decimal):
            res = float(o)
        elif isinstance(o, datetime.datetime):
            res = calendar.timegm(o.timetuple())
        elif isinstance(o, uuid.UUID):
            res = str(o)
        else:
            res = o
        return res

    if isinstance(raw_response, str):
        clean_response = prepare_for_json(raw_response)
    elif isinstance(raw_response, dict):
        clean_response = {k: map_response(v) for k, v in raw_response.items()}
    elif isinstance(raw_response, collections.Iterable):
        clean_response = [map_response(i) for i in raw_response]
    else:
        clean_response = prepare_for_json(raw_response)

    return clean_response
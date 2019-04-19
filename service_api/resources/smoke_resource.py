from sanic.views import HTTPMethodView
from sanic.response import json


class SmokeResource(HTTPMethodView):
    async def get(self, request):
        return json({'Result': 'This is a smoke view'})

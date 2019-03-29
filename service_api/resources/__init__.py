from sanic.views import HTTPMethodView
from sanic.response import json


class SmokeView(HTTPMethodView):
    async def get(self, request):
        return json({'This is: ': 'smoke view'})
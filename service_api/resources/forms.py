import uuid
from marshmallow import Schema, fields, validate, pre_load, pre_dump, ValidationError


class ClientSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=False)
    email = fields.Str(required=False,
                       validate=validate.Email(error='Not a valid email address'))
    age = fields.Int(required=False)
    address = fields.Str(required=False)

    @pre_load
    def name_input(self, data):
        data['name'] = (' ').join([word.lower().capitalize()
                                   for word in data['name'].split()])

    @pre_dump
    def validate_output(self, data):
        try:
            uuid.UUID(data['id'])
        except ValueError as err:
            raise ValidationError(err.args)
        except KeyError as err:
            raise ValidationError(err.args)



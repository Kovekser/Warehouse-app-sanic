import uuid
from marshmallow import Schema, fields, validate, pre_load, pre_dump, ValidationError


class BaseSchema(Schema):
    id = fields.UUID(required=True)

    @pre_dump
    def validate_output(self, data):
        try:
            uuid.UUID(data['id'])
        except ValueError as err:
            raise ValidationError(err.args)
        except KeyError as err:
            raise ValidationError(err.args)


class ClientSchema(BaseSchema):
    name = fields.Str(required=False)
    email = fields.Str(required=False,
                       validate=validate.Email(error='Not a valid email address'))
    age = fields.Int(required=False)
    address = fields.Str(required=False)

    @pre_load
    def name_input(self, data):
        data['name'] = ' '.join([word.lower().capitalize()
                                 for word in data['name'].split()])


class ParceltypeSchema(BaseSchema):
    type_name = fields.Str(required=True)

    @pre_load
    def type_input(self, data):
        try:
            data['type_name'] = data['type_name'].lower()
        except KeyError:
            pass


class StorageSchema(BaseSchema):
    address = fields.Str(required=False)
    max_weight = fields.Int(required=False)
    max_capacity = fields.Int(required=False)

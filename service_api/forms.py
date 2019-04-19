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
    type_name = fields.Str(required=True, validate=validate.Length(min=1))

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


class ParcelSchema(BaseSchema):
    description = fields.Str(required=False)
    type_id = fields.UUID(required=True)
    weight = fields.Decimal(required=True)
    cost = fields.Decimal(required=True)
    supply_id = fields.UUID(required=True)

    @pre_load
    def validate_weight(self, data):
        try:
            if data['weight'] > 1000:
                raise ValidationError('Parcel weight can\'t be greater than 1000')
        except KeyError:
            pass
        except TypeError:
            pass


class SupplySchema(BaseSchema):
    from_storage = fields.UUID(required=True)
    to_storage = fields.UUID(required=True)
    status = fields.Str(required=False)
    client_id = fields.UUID(required=True)
    send_date = fields.DateTime(required=True, format='%Y-%m-%d')
    received_date = fields.DateTime(required=False, format='%Y-%m-%d')

    @pre_load
    def validate_received_date(self, data):
        try:
            if data['received_date'] < data['send_date']:
                raise ValidationError('Receive date can\'t be earlier than send date!')
        except KeyError:
            pass
        except TypeError:
            pass

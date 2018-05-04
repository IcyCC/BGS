from marshmallow import Schema, fields, validates, ValidationError, post_load
class UserValidation(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
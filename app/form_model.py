from marshmallow import Schema, fields, validates, ValidationError, post_load, validates_schema
class UserValidation(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email()
    tel = fields.String(required=True)
    hospital = fields.String(required=True)
    lesion = fields.String()

    @validates_schema
    def validate_tel(self, data):
        if not data['tel'].isdigit():
            raise ValidationError('tel must be made by number')
        if len(data['tel'])>11 or len(data['tel'])<7:
            raise ValidationError('the length of tel is wrong')

class ChangeUserValidation(Schema):
    username = fields.String()
    password = fields.String()
    email = fields.Email()
    tel = fields.String()
    hospital = fields.String()
    lesion = fields.String()

    @validates_schema
    def validate_tel(self, data):
        if not data['tel'].isdigit():
            raise ValidationError('tel must be made by number')
        if len(data['tel']) > 12 or len(data['tel']) < 7:
            raise ValidationError('the length of tel is wrong')

class PatientValidation(Schema):
    patient_name = fields.String(required=True)
    sex = fields.String(required=True)
    tel = fields.String(required=True)
    id_number = fields.String(required=True)
    age = fields.Integer(required=True)
    doctor_name = fields.String(required=True)

    @validates_schema
    def validate_tel(self, data):
        if not data['tel'].isdigit():
            raise ValidationError('tel must be made by number')

    @validates_schema
    def validate_sex(self, data):
        if data['sex'] != '男' or data['sex'] != '女':
            raise ValidationError('sex is wrong')

class OperatorPasswordValidation(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class DataValidation(Schema):
    sn = fields.String(required=True)
    glucose = fields.Integer(required=True)

    @validates_schema
    def validate_sn(self, data):
        if len(data['sn']) != 8:
            raise ValidationError('the length of sn is wrong')

class AccuchekValidation(Schema):
    sn = fields.String(required=True)
    bed_id = fields.Integer()

    @validates_schema
    def validate_sn(self, data):
        if len(data['sn']) != 8:
            raise ValidationError('the length of sn is wrong')

class BedValidation(Schema):
    id_number = fields.Integer()
    sn = fields.String()

    @validates_schema
    def validate_sn(self, data):
        if len(data['sn']) != 8:
            raise ValidationError('the length of sn is wrong')


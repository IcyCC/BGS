from marshmallow import Schema, fields, validates, ValidationError, post_load, validates_schema
class OperatorValidation(Schema):
    operator_name = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(allow_none=True)
    tel = fields.String(required=True)
    hospital = fields.String(required=True)
    lesion = fields.String(allow_none=True)
    operator_id = fields.Integer(allow_none=True)
    active = fields.Boolean(allow_none=True)
    office = fields.String(required=True)

    @validates('active')
    def validate_active(self, value):
        if value is not None:
            raise ValidationError('active should not be posted')

    @validates('operator_id')
    def validate_operator_id(self, value):
        if value is not None:
            raise ValidationError('operator_id should not be posted')

    @validates('tel')
    def validate_tel(self, value):
        if not value.isdigit():
            raise ValidationError('tel must be made by number')
        if len(value)>11 or len(value)<7:
            raise ValidationError('the length of tel is wrong')

class GetOperatorValidation(Schema):
    operator_name = fields.String(allow_none=True)
    password = fields.String(allow_none=True)
    email = fields.Email(allow_none=True)
    tel = fields.String(allow_none=True)
    hospital = fields.String(allow_none=True)
    lesion = fields.String(allow_none=True)
    operator_id = fields.Integer(allow_none=True)
    active = fields.Boolean(allow_none=True)
    office = fields.String(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('password')
    def validate_password(self, value):
        if value is not None:
            raise ValidationError('password should not be posted')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

class ChangeOperatorValidation(Schema):
    operator_name = fields.String(allow_none=True)
    password = fields.String(allow_none=True)
    email = fields.Email(allow_none=True)
    tel = fields.String(allow_none=True)
    hospital = fields.String(allow_none=True)
    lesion = fields.String(allow_none=True)
    operator_id = fields.Integer(allow_none=True)
    active = fields.Boolean(allow_none=True)
    office = fields.String(allow_none=True)

    @validates('password')
    def validate_password(self, value):
        if value is not None:
            raise ValidationError('password should not be posted')

    @validates('active')
    def validate_active(self, value):
        if value is not None:
            raise ValidationError('active should not be posted')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('operator_id')
    def validate_operator_id(self, value):
        if value is not None:
            raise ValidationError('operator_id should not be posted')

class OperatorPasswordValidation(Schema):
    operator_name = fields.String()
    password = fields.String(required=True)

class GetAccuchekValidation(Schema):
    accuchek_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    bed_id = fields.Integer(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

class AccuchekValidation(Schema):
    accuchek_id = fields.Integer(allow_none=True)
    sn = fields.String(required=True)
    bed_id = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('accuchek_id')
    def validate_accuchek_id(self, value):
        if value is not None:
            raise ValidationError('accuchek_id should not be posted')

class ChangeAccuchekValidation(Schema):
    accuchek_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    bed_id = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('accuchek_id')
    def validate_accuchek_id(self, value):
        if value is not None:
            raise ValidationError('accuchek_id should not be posted')

class GetBedValidation(Schema):
    bed_id = fields.Integer(allow_none=True)
    id_number = fields.String(allow_none=True)
    sn = fields.String(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

class BedValidation(Schema):
    bed_id = fields.Integer(allow_none=True)
    id_number = fields.String(allow_none=True)
    sn = fields.String(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('bed_id')
    def validate_bed_id(self, value):
        if value is not None:
            raise ValidationError('bed_id should not be posted')

class ChangeBedValidation(Schema):
    bed_id = fields.Integer(allow_none=True)
    id_number = fields.String(allow_none=True)
    sn = fields.String(allow_none=True)
    history_id = fields.Integer(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    tel = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    doctor_name = fields.String(allow_none=True)

    @validates('sex')
    def validate_sex(self, value):
        if value is not None and value != '男' or value is not None and value != '女':
            raise ValidationError('sex is wrong')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('bed_id')
    def validate_bed_id(self, value):
        if value is not None:
            raise ValidationError('bed_id should not be posted')

    @validates('patient_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('patient_id should not be posted')

    @validates('history_id')
    def validate_history_id(self, value):
        if value is not None:
            raise ValidationError('history_id should not be posted')

    @validates('date')
    def validate_date(self, value):
        if value is not None:
            raise ValidationError('date should not be posted')

    @validates('time')
    def validate_time(self, value):
        if value is not None:
            raise ValidationError('time should not be posted')
        
class BedMoreDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    glucose = fields.Float(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')
    


class PatientValidation(Schema):
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(required=True)
    sex = fields.String(required=True)
    tel = fields.String(required=True)
    id_number = fields.String(required=True)
    age = fields.Integer(required=True)
    doctor_name = fields.String(allow_none=True)

    @validates('patient_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('patient_id should not be posted')

    @validates('tel')
    def validate_tel(self, value):
        if not value.isdigit():
            raise ValidationError('tel must be made by number')
        if len(value) > 11 or len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value != '男' and value != '女':
            raise ValidationError('sex is wrong')


class GetPatientValidation(Schema):
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    tel = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    doctor_name = fields.String(allow_none=True)
    per_page = fields.Integer(allow_none=True)
    limit = fields.Integer(allow_none=True)

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value is not None and value != '男' and value != '女':
            raise ValidationError('sex is wrong')

class ChangePatientValidation(Schema):
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    tel = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    doctor_name = fields.String(allow_none=True)

    @validates('patient_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('patient_id should not be posted')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value is not None and value != '男' and value != '女':
            raise ValidationError('sex is wrong')

class PatientDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    glucose = fields.Float(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

class PatientHistoryValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    time = fields.String(allow_none=True)
    date = fields.Date(allow_none=True)
    glucose = fields.Float(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    tel = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    doctor_name = fields.String(allow_none=True)
    max_glucose = fields.Float(allow_none=True)
    min_glucose = fields.Float(allow_none=True)
    begin_time = fields.String(allow_none=True)
    end_time = fields.String(allow_none=True)
    begin_date = fields.Date(allow_none=True)
    end_date = fields.Date(allow_none=True)
    max_age = fields.Integer(allow_none=True)
    min_age = fields.Integer(allow_none=True)

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value is not None and value != '男' and value != '女':
            raise ValidationError('sex is wrong')

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

class BedHistoryValidation(Schema):
    history_id = fields.Integer(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    bed_id = fields.Integer(required=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('history_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('history_id should not be posted')

class GetBedHistoryValidation(Schema):
    history_id = fields.Integer(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    bed_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('history_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('history_id should not be posted')

class ChangeBedHistoryValidation(Schema):
    history_id = fields.Integer(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    bed_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('history_id')
    def validate_patient_id(self, value):
        if value is not None:
            raise ValidationError('history_id should not be posted')


class DataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(required=True)
    glucose = fields.Float(required=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    hidden = fields.Boolean(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('data_id')
    def validate_data_id(self, value):
        if value is not None:
            raise ValidationError('data_id should not be posted')

class DataArtificialValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(required=True)
    glucose = fields.Float(required=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    patient_id = fields.Integer(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    tel = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    doctor_name = fields.String(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')


    @validates('data_id')
    def validate_data_id(self, value):
        if value is not None:
            raise ValidationError('data_id should not be posted')

    @validates('patient_id')
    def validate_patient_id(self, value):
        if value is not None:
            return ValidationError('patient_id should be posted')\
        

    @validates('sex')
    def validate_sex(self, value):
        if value != '男' or value != '女':
            raise ValidationError('sex is wrong')

class GetDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    glucose = fields.Float(allow_none=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    per_page = fields.Integer(allow_none=True)
    limit = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

class GetSpareDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    tel = fields.String(allow_none=True)
    doctor = fields.String(allow_none=True)
    time = fields.Time(aillow_none=True)
    date = fields.Date(allow_none=True)
    glucose = fields.Float(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    limit = fields.Integer(allow_none=True)
    per_page = fields.Integer(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if value is not None and len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value is not None and value != '男' and value != '女':
            raise ValidationError('sex is wrong')
        
class ChangeSpareDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(allow_none=True)
    id_number = fields.String(allow_none=True)
    patient_name = fields.String(allow_none=True)
    sex = fields.String(allow_none=True)
    age = fields.Integer(allow_none=True)
    tel = fields.String(allow_none=True)
    doctor = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    glucose = fields.Float(allow_none=True)
    hidden = fields.Boolean(allow_none=True)
    
    @validates('data_id')
    def validate_data_id(self, value):
        if value is not None:
            raise ValidationError('data_id should not be posted')

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('tel')
    def validate_tel(self, value):
        if value is not None and not value.isdigit():
            raise ValidationError('tel must be made by number')
        if value is not None and len(value) > 11 or value is not None and len(value) < 7:
            raise ValidationError('the length of tel is wrong')

    @validates('sex')
    def validate_sex(self, value):
        if value != '男' or value != '女':
            raise ValidationError('sex is wrong')
        
class ChangeDataValidation(Schema):
    data_id = fields.Integer(allow_none=True)
    sn = fields.String(required=True)
    glucose = fields.Float(required=True)
    id_number = fields.String(allow_none=True)
    time = fields.Time(allow_none=True)
    date = fields.Date(allow_none=True)
    hidden = fields.Boolean(allow_none=True)

    @validates('sn')
    def validate_sn(self, value):
        if len(value) != 8:
            raise ValidationError('the length of sn is wrong')

    @validates('data_id')
    def validate_data_id(self, value):
        if value is not None:
            raise ValidationError('data_id should not be posted')






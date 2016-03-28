from mongoengine import Document, DateTimeField, StringField, FloatField, IntField


class TimeLog(Document):
    request_time = DateTimeField(required=True)
    url = StringField(required=True, max_length=255)
    response_time = FloatField(required=True)
    response_code = IntField(required=True)
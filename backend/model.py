from mongoengine import (Document, StringField, DateTimeField, IntField, ReferenceField)
from datetime import datetime


class Image(Document):
    filename = StringField()
    path = StringField()
    extension = StringField()
    uploaded_on = DateTimeField(default=datetime.now())
    created_at = DateTimeField(default=datetime.now())
    

class ObjectDetected(Document):
    image = ReferenceField(Image, required=True)
    xmin = IntField()
    ymin = IntField()
    xmax = IntField()
    ymax = IntField()
    type = StringField()
    created_at = DateTimeField(default=datetime.now())

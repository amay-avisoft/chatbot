from mongoengine import Document, StringField, ListField, FloatField

class TextDocument(Document):
    content = StringField(required=True)
    source_url = StringField()
    embedding = ListField(FloatField())
    
    meta = {
        'collection': 'documents',
        'indexes': [
            {
                'fields': ['embedding'],
                'cls': False,
                'weights': {'embedding': 1},
                'default_language': 'english',
            }
        ]
    }
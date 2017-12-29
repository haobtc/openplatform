from django.db import models
import json

class BixinDecimalField(models.DecimalField):
    def __init__(self, **kw):
        kw.setdefault('max_digits', 65)
        kw.setdefault('decimal_places', 30)
        super(BixinDecimalField, self).__init__(**kw)

class JSONField(models.TextField):
    def __init__(self, **kw):
        kw.setdefault('default', json.dumps({}))
        super(JSONField, self).__init__(**kw)

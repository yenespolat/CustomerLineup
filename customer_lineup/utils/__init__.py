from datetime import date

from flask.json import JSONEncoder
from werkzeug.datastructures import MultiDict


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class LayoutPI:
    def __init__(self, title):
        self.title = title
        self.website_name = "Website name"
        self.short_website_name = "Short website name"


class FormPI(LayoutPI):
    def __init__(self, form, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form = form
        self.errors = []
        for field in form:
            self.errors += field.errors


def flask_form_to_dict(request_form: MultiDict, exclude=None, boolean_fields: list = []):
    if exclude is None:
        exclude = []

    result = {
        key: request_form.getlist(key)[0] if len(request_form.getlist(key)) == 1 else request_form.getlist(key)
        for key in request_form
        if key not in exclude and not (len(request_form.getlist(key)) == 1 and request_form.getlist(key)[0] == "")
    }
    for i in boolean_fields:
        if result.get(i):
            result[i] = True
        else:
            result[i] = False
    result.pop('submit', None)
    result.pop('csrf_token', None)

    return result

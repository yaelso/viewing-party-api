from flask import abort, make_response

def validate_model(cls, model_id):
    '''Validates model instance based on provided model `cls` and id.'''

    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": f"Class `{cls.__name__}` ID `{model_id}` invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": f"Class `{cls.__name}` ID `{model_id}` not found"}, 404))

    return model

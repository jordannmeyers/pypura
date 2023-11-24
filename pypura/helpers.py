def is_primitive(obj):
    return not hasattr(obj, '__dict__')
from typing import Any, Type

def args_cast(
        schema: dict[str, tuple[str, Type]], 
        data: dict[str, Any]
        ) -> dict[str, Any]:

    def err_message(missed: set[str], extra: set[str]) -> str:
        _template = "Incompatible dict given. Missing: {}, Extra: {}"
        return _template.format(missed or None, extra or None)
    
    _expected, _provided = set(schema.keys()), set(data.keys())
    _missed, _extra = _expected - _provided, _provided - _expected
    if _missed | _extra:
        raise ValueError(err_message(_missed, _extra))
    
    args = {}
    for key, (_alias, _type) in schema.items():
        args[_alias] = _type(data[key])
    return args

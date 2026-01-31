from datetime import datetime
from typing import Any

def json_safe(obj: Any) :
    if isinstance(obj, datetime) :
        return obj.isoformat()
    return str(obj)
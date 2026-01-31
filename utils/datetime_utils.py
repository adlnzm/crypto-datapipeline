from datetime import datetime

def parse_iso_ts(value) :
    """
    Convert ISO 8601 String
    
    into python datetime
    """
    if not value :
        return None
    
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
REQUIRED_FIELDS = [
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "total_volume",
    "last_updated",
]

def validate_market_record(record: dict) -> bool :
    try :
        return (
            all(field in record and record[field] is not None 
                   for field in REQUIRED_FIELDS)
            and record["current_price"] > 0
            and record["market_cap"] > 0 
            and record["total_volume"] >= 0
        )
    except (TypeError, KeyError) :
        return False
def generate_delta(config: dict, patched: dict) -> dict:
    additions = []
    deletions = []
    updates = []

    for key in patched:
        if key not in config:
            additions.append({
                "key": key,
                "value": patched[key],
            })
        elif patched[key] != config[key]:
            updates.append({
                "key": key,
                "from": config[key],
                "to": patched[key],
            })
        
    for key in config:
        if key not in patched:
            deletions.append(key)

    return {
        "additions": additions,
        "deletions": deletions,
        "updates": updates,
    }

def apply_delta(config: dict, delta: dict) -> dict:
    result = dict(config)

    for key in delta["deletions"]:
        if key in result:
            del result[key]

    for update in delta["updates"]:
        result[update["key"]] = update["to"]

    for addition in delta["additions"]:
        result[addition["key"]] = addition["value"]
        
    return result

def _parse_multiplicity(value: str) -> tuple[str, str]:
    if ".." in value:
        min_value, max_value = value.split("..")
        return min_value, max_value
    return value, value

def _find_class_multiplicity(class_name: str, model: dict) -> tuple[str, str] | None:
    for aggregation in model["aggregations"]:
        if aggregation["source"] == class_name:
            return _parse_multiplicity(aggregation["sourceMultiplicity"])
    return None
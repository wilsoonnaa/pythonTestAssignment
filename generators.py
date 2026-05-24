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

def generate_meta_json(model: dict, children_by_parent: dict) -> list:
    meta = []

    class_multiplicities = _build_class_multiplicities(model)

    ordered_classes = _post_order_classes(model["root_class"], children_by_parent)
    for class_name in ordered_classes:
        class_data = model["classes"][class_name]
        parameters = []

        for attribute in class_data["attributes"]:
            parameters.append({
                "name": attribute["name"],
                "type": attribute["type"],
            })

        for child in children_by_parent.get(class_name, []):
            parameters.append({
                "name": child["child"],
                "type": "class",
            })

        entry = {
            "class": class_name,
            "documentation": class_data["documentation"],
            "isRoot": class_data["isRoot"],
        }

        if class_name in class_multiplicities:
            min_value, max_value = class_multiplicities[class_name]
            entry["max"] = max_value
            entry["min"] = min_value

        entry["parameters"] = parameters
        meta.append(entry)

    return meta  


from helper_functions import build_class_multiplicities, post_order_classes


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
        result.pop(key, None)

    for update in delta["updates"]:
        result[update["key"]] = update["to"]

    for addition in delta["additions"]:
        result[addition["key"]] = addition["value"]

    return result


def generate_meta_json(model: dict, children_by_parent: dict) -> list:
    meta = []
    class_multiplicities = build_class_multiplicities(model)
    ordered_classes = post_order_classes(model["root_class"], children_by_parent)

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


def generate_config_xml(model: dict, children_by_parent: dict) -> str:
    classes = model["classes"]

    def build(class_name: str, indent_level: int = 0) -> str:
        indent = "    " * indent_level
        inner_indent = "    " * (indent_level + 1)

        lines = [f"{indent}<{class_name}>"]

        for attribute in classes[class_name]["attributes"]:
            lines.append(
                f"{inner_indent}<{attribute['name']}>"
                f"{attribute['type']}</{attribute['name']}>"
            )

        for child in children_by_parent.get(class_name, []):
            lines.append(build(child["child"], indent_level + 1))

        lines.append(f"{indent}</{class_name}>")
        return "\n".join(lines)

    return build(model["root_class"])

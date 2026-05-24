def _parse_multiplicity(value: str) -> tuple[str, str]:
    if ".." in value:
        min_value, max_value = value.split("..", 1)
        return min_value, max_value
    return value, value


def build_class_multiplicities(model: dict) -> dict:
    lookup = {}
    for aggregation in model["aggregations"]:
        source = aggregation["source"]
        lookup[source] = _parse_multiplicity(aggregation["sourceMultiplicity"])
    return lookup


def post_order_classes(root_class: str, children_by_parent: dict) -> list:
    ordered = []

    def visit(class_name: str) -> None:
        for child in children_by_parent.get(class_name, []):
            visit(child["child"])
        ordered.append(class_name)

    visit(root_class)
    return ordered

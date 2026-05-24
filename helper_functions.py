"""Вспомогательные функции для работы с UML-моделью.

_parse_multiplicity — разбирает строку кратности вида '0..42' или '1'
    на пару (min, max);
build_class_multiplicities — для каждого дочернего класса возвращает
    минимальную и максимальную кратность из агрегаций;
post_order_classes — возвращает имена классов в пост- порядке обхода
    (сначала дочерние, затем родительские).
"""
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

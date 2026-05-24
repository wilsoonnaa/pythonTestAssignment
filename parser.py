import xml.etree.ElementTree as ET
from pathlib import Path

def parse_model(xml_path: Path) -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    classes = {}
    aggregations = []
    root_class = None

    for class_element in root.findall("Class"):
        name = class_element.get("name")
        documentation = class_element.get("documentation", "")
        is_root = class_element.get("isRoot") == "true"

        attributes = []
        for attribute_element in class_element.findall("Attribute"):
            attributes.append({
                "name": attribute_element.get("name"),
                "type": attribute_element.get("type"),
            })

        classes[name] = {
            "documentation": documentation,
            "isRoot": is_root,
            "attributes": attributes,
        }

        if is_root:
            root_class = name

    for aggregation_element in root.findall("Aggregation"):
        aggregations.append({
            "source": aggregation_element.get("source"),
            "target": aggregation_element.get("target"),
            "sourceMultiplicity": aggregation_element.get("sourceMultiplicity"),
            "targetMultiplicity": aggregation_element.get("targetMultiplicity"),
        })

    return {
        "classes": classes,
        "aggregations": aggregations,
        "root_class": root_class,
    }


def get_children_by_parent(model: dict) -> dict:
    children_by_parent = {}

    for aggregation in model["aggregations"]:
        parent = aggregation["target"]
        child = aggregation["source"]

        if parent not in children_by_parent:
            children_by_parent[parent] = []

        children_by_parent[parent].append({
            "child": child,
            "source_multiplicity": aggregation["sourceMultiplicity"],
            "target_multiplicity": aggregation["targetMultiplicity"],
        })

    return children_by_parent

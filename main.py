import json
from pathlib import Path

from parser import parse_model, get_children_by_parent
from generators import (
    generate_delta,
    apply_delta,
    generate_meta_json,
    generate_config_xml,
)

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("out")

INPUT_XML = INPUT_DIR / "impulse_test_input.xml"
CONFIG_JSON = INPUT_DIR / "config.json"
PATCHED_CONFIG_JSON = INPUT_DIR / "patched_config.json"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict | list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def write_text(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def verify_res_patched_config(output_path: Path, reference_path: Path) -> None:
    applied = load_json(output_path)
    reference = load_json(reference_path)

    if applied == reference:
        print("Delta application verified against patched_config.json")
        return

    differing_keys = [
        key for key in set(applied) | set(reference)
        if applied.get(key) != reference.get(key)
    ]
    print(
        f"Delta verification failed: {len(differing_keys)} "
        f"parameter(s) do not match patched_config.json"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    model = parse_model(INPUT_XML)
    children_by_parent = get_children_by_parent(model)

    config = load_json(CONFIG_JSON)
    patched = load_json(PATCHED_CONFIG_JSON)

    config_xml = generate_config_xml(model, children_by_parent)
    meta_json = generate_meta_json(model, children_by_parent)
    delta = generate_delta(config, patched)
    result = apply_delta(config, delta)

    write_text(OUTPUT_DIR / "config.xml", config_xml)
    write_json(OUTPUT_DIR / "meta.json", meta_json)
    write_json(OUTPUT_DIR / "delta.json", delta)
    write_json(OUTPUT_DIR / "res_patched_config.json", result)

    print(
        f"Generated 4 files in {OUTPUT_DIR}/: "
        "config.xml, meta.json, delta.json, res_patched_config.json"
    )

    verify_res_patched_config(
        OUTPUT_DIR / "res_patched_config.json",
        PATCHED_CONFIG_JSON,
    )


if __name__ == "__main__":
    main()

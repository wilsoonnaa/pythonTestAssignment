import json
from pathlib import Path

from parser import parse_model, get_children_by_parent
from generators import generate_delta, apply_delta, generate_meta_json

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("out")

INPUT_XML = INPUT_DIR / "impulse_test_input.xml"
CONFIG_JSON = INPUT_DIR / "config.json"
PATCHED_CONFIG_JSON = INPUT_DIR / "patched_config.json"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[OK] {path.name}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    model = parse_model(str(INPUT_XML))
    children_by_parent = get_children_by_parent(model)

    config = load_json(CONFIG_JSON)
    patched = load_json(PATCHED_CONFIG_JSON)

    meta_json = generate_meta_json(model, children_by_parent)
    write_json(OUTPUT_DIR / "meta.json", meta_json)

    print("\n--- meta.json class order ---")
    for entry in meta_json:
        min_max = ""
        if "min" in entry and "max" in entry:
            min_max = f" (min={entry['min']}, max={entry['max']})"
        print(f"  {entry['class']}{min_max}")

    delta = generate_delta(config, patched)
    write_json(OUTPUT_DIR / "delta.json", delta)

    result = apply_delta(config, delta)
    write_json(OUTPUT_DIR / "res_patched_config.json", result)

    print("\n--- delta summary ---")
    print(f"  additions: {len(delta['additions'])}")
    print(f"  deletions: {len(delta['deletions'])}")
    print(f"  updates:   {len(delta['updates'])}")

    if result == patched:
        print("\n[PASS] res_patched_config.json matches patched_config.json")
    else:
        extra = set(result) - set(patched)
        missing = set(patched) - set(result)
        print(f"\n[FAIL] mismatch — extra keys: {extra}, missing keys: {missing}")


if __name__ == "__main__":
    main()

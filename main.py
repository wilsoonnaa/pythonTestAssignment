import json
from parser import parse_model, get_children_by_parent
from generators import generate_delta


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_json("input/config.json")
    patched = load_json("input/patched_config.json")

    delta = generate_delta(config, patched)
    print(json.dumps(delta, indent=4))


if __name__ == "__main__":
    main()
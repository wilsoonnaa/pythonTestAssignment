import json
from parser import parse_model

INPUT_XML_PATH = "input/impulse_test_input.xml"

def main():
    model = parse_model(INPUT_XML_PATH)
    print(json.dumps(model, indent=2))

if __name__ == "__main__":
    main()
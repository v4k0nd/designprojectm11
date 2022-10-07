import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from test_api import *

SCHEMA_PATH = "/mnt/c/Users/chris/Documents/University/design project/data/schemas-main/schema_dsi_algorithm_predictions - Modified.json"


def load_schema():
    with open(SCHEMA_PATH) as json_file:
        return json.load(json_file)


def test_json_multiple_images():
    json_schema = load_schema()
    try:
        validate(api_testing("dataset-1-5"), json_schema)
        assert True is True
    except ValidationError:
        assert False is False



def test_json_single_image():
    json_schema = load_schema()
    try:
        validate(api_testing("dataset-1"), json_schema)
        assert True is True
    except ValidationError:
        assert False is False



def test_json_blank_image():
    json_schema = load_schema()
    try:
        validate(api_testing("dataset-blank"), json_schema)
        assert True is True
    except ValidationError:
        assert False is False






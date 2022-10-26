import json
import os

import pytest


class Data:
    def __init__(self, root_path):
        self.root_path = root_path

    def load(self, *path):
        path = os.path.join(self.root_path, *path)
        json_path = path + ".json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                return json.load(f)


@pytest.fixture(scope="session")
def data():
    return Data(
        root_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    )

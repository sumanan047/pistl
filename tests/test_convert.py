import os
import pytest
from pistl import converter


@pytest.fixture
def step_file():
    return 'assets/test.stp'


def test_convert(step_file):
    converter.convert(input_file=step_file, output_file="assets/test.stl")
    assert os.path.exists('assets/test.stl'), "Failed to write the stl file."

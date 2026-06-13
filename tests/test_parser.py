#!/usr/bin/env python3

import pytest
from unittest.mock import patch, mock_open
from src.parser import get_functions, get_prompts, get_params


def test_get_functions_valid() -> None:
    """
    Test valid function definitions loading and Pydantic validation.

    Return:
        None
    """
    valid_json = (
        '[\n'
        '  {\n'
        '    "name": "fn_add",\n'
        '    "description": "Add numbers",\n'
        '    "parameters": {\n'
        '      "a": {"type": "integer"}\n'
        '    },\n'
        '    "returns": {"type": "integer"}\n'
        '  }\n'
        ']'
    )

    with patch("builtins.open", mock_open(read_data=valid_json)):
        funcs = get_functions("dummy_path.json")
        assert funcs is not None
        assert len(funcs) == 1
        assert funcs[0].name == "fn_add"


def test_get_functions_invalid_pattern() -> None:
    """
    Test that an invalid function name triggers a system exit.

    Return:
        None
    """
    invalid_json = (
        '[\n'
        '  {\n'
        '    "name": "invalid_name_without_prefix",\n'
        '    "description": "Missing prefix",\n'
        '    "parameters": {},\n'
        '    "returns": {"type": "string"}\n'
        '  }\n'
        ']'
    )

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with pytest.raises(SystemExit) as exc_info:
            get_functions("dummy_path.json")
        assert exc_info.value.code == 1


def test_get_prompts_valid() -> None:
    """
    Test valid prompts loading and structural validation.

    Return:
        None
    """
    valid_json = '[\n  {"prompt": "Hello"},\n  {"prompt": "World"}\n]'

    with patch("builtins.open", mock_open(read_data=valid_json)):
        prompts = get_prompts("dummy_path.json")
        assert prompts is not None
        assert len(prompts) == 2
        assert prompts[0].prompt == "Hello"


def test_get_params_integration() -> None:
    """
    Test that get_params accurately aggregates function and prompt data.

    Return:
        None
    """
    funcs_json = '[]'
    prompts_json = '[]'

    with patch("builtins.open", mock_open()) as mocked_file:
        mocked_file.side_effect = [
            mock_open(read_data=funcs_json).return_value,
            mock_open(read_data=prompts_json).return_value,
        ]

        res = get_params("funcs.json", "prompts.json")
        assert "functions" in res
        assert "prompts" in res

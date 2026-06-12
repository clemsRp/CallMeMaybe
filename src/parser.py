#!/usr/bin/env python3

import sys
import json
from typing import Any
from src.models import Functions, Prompts


def invalid_format() -> None:
    '''
    Stop the program due to a wrong parameters format.

    Args:
        None
    Return:
        None
    '''
    print(
        "Invalid parameters\n"
        "format must be 'uv run python -m src "
        "[--functions_definition <functions_definition_file>]  "
        "[--input <input_file>] [--output <output_file>]'"
    )
    sys.exit(1)


def invalid_file(filename: str, error: Exception) -> None:
    '''
    Stop the program due to a wrong file format.

    Args:
        filename: str = The error's file
        error: Exception = The Exception catch
    Return:
        None
    '''
    print(f"Error in {filename}:\n{error}")
    sys.exit(1)


def get_functions(filename: str) -> dict[Any, Any] | None:
    '''
    Return the dict corresponding to
    the functions definitions
    converted from str to JSON/dict

    Args:
        filename: str = path to the input file
    Return:
        dict[Any, Any]
    '''
    try:
        with open(filename, 'r') as f:
            content: dict = json.load(f)
            res: Functions = Functions(functions=content)
            return res.functions
    except Exception as e:
        invalid_file(filename, e)
        return None


def get_prompts(filename: str) -> list[dict[str, str]] | None:
    '''
    Return the dict corresponding to the prompts
    converted from str to JSON/dict

    Args:
        filename: str = path to the input file
    Return:
        res: list[dict[str, str]] = All the prompts
    '''
    try:
        with open(filename, 'r') as f:
            content: dict = json.load(f)
            res = Prompts(prompts=content)
            return res.prompts
    except Exception as e:
        invalid_file(filename, e)
        return None


def get_params(
            functions_path: str,
            input_file: str
        ) -> dict[str, Any]:
    '''
    Return the paths for the input and output files

    Args:
        functions_path: str = The path for the functions definitions
        input_file: str = The path for the prompts file
    Return:
        dict[str, Any] =
            - functions definitions
            - prompts
    '''

    # TODO: Implement Pydantic
    pass

    return {
        "functions": get_functions(functions_path),
        "prompts": get_prompts(input_file)
    }

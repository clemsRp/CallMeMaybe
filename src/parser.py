#!/usr/bin/env python3

import sys
import json
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from src.models import Function, Functions, Prompt, Prompts


def handle_error(error_type: str, error: str) -> None:
    '''
    Print the errors and quit the programm using sys.exit()

    Args:
        error_type: str = The type of the error
        error: str = The error to print
    Return:
        None
    '''
    console: Console = Console()
    error_message: str = f"[bold white]Details:[/bold white] {str(error)}"
    error_panel = Panel(
        error_message,
        title=f"[bold red]{error_type}[/bold red]",
        title_align="left",
        border_style="red bold",
        box=ROUNDED,
        expand=False
    )
    console.print(error_panel)
    sys.exit(1)


def get_functions(filename: str) -> list[Function]:
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
            content: list[Function] = json.load(f)
            res: Functions = Functions(functions=content)
            return res.functions

    except FileNotFoundError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' doesn't exist:\n{e.args[1] if e.args else str(e)}"
        )
        return []

    except PermissionError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' doesn't have the correct rights:\n"
            f"{e.args[1] if e.args else str(e)}"
        )
        return []

    except json.decoder.JSONDecodeError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' isn't well formated:\n"
            f"Check for line {e.lineno} column {e.colno}"
        )
        return []

    except Exception as e:
        handle_error(
            "Invalid file",
            f" Error in '{filename}':\n{e.args[1] if e.args else str(e)}"
        )
        return []


def get_prompts(filename: str) -> list[Prompt]:
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
            content: list[Prompt] = json.load(f)
            res: Prompts = Prompts(prompts=content)
            return res.prompts

    except FileNotFoundError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' doesn't exist:\n{e.args[1] if e.args else str(e)}"
        )
        return []

    except PermissionError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' doesn't have the correct rights:\n"
            f"{e.args[1] if e.args else str(e)}"
        )
        return []

    except json.decoder.JSONDecodeError as e:
        handle_error(
            "Invalid file",
            f"'{filename}' isn't well formated:\n"
            f"Check for line {e.lineno} column {e.colno}"
        )
        return []

    except Exception as e:
        handle_error(
            "Invalid file",
            f" Error in '{filename}':\n{e.args[1] if e.args else str(e)}"
        )
        return []


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
    return {
        "functions": get_functions(functions_path),
        "prompts": get_prompts(input_file)
    }

#!/usr/bin/env python3

from typing import Any
from src.parser import handle_error


def get_context_fn_name(functions: str) -> str:
    '''
    Get the context to correctly 'set' the LLM for the fn_name

    Args:
        fumctions: str = The functions definitions parsed in the input file
    Return:
        context: str = The LLM context for the fn_name part
    '''
    context: str = "Chose one fn_name in:"
    context += functions

    return context


def get_context_args(functions: list[dict[str, Any]], fn_name: str) -> str:
    '''
    Get the context to correctly 'set' the LLM for the args

    Args:
        functions: list[dict[str, Any]] =
            The functions definitions parsed in the input file
        fn_name: str = The function chose by the LLM
    Return:
        context: str = The LLM context for the args part
    '''
    try:
        func_def: dict[str, Any] = [
            func for func in functions
            if func["name"] == fn_name
        ][0]

    except IndexError:
        handle_error(
            "Missing function",
            f"Didn't find the '{fn_name}' function."
        )

    context = f"Function {func_def['name']}:\n"

    context += f"Description: {func_def['description']}\n"
    context += "Parameters:\n"
    for param_name, param_info in func_def.get('parameters', {}).items():
        desc = param_info.get('description', '')
        context += f"- {param_name} ({param_info.get('type')}): {desc}\n"

    context += "\nGenerate arguments for this function:"

    return context

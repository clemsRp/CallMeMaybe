#!/usr/bin/env python3

from llm_sdk.llm_sdk import Small_LLM_Model
from src.context import get_context_args
from src.fill_response import get_fn_name, get_args


def get_args_types(functions: list[dict], fn_name: str) -> dict[str, str]:
    '''
    Return the list of the keys which are inside the fn_name arguments

    Args:
        functions: list[dict] = All the accessible function definitions
        fn_name: str = The currently use function name
    Return:
        res: dict[str, str] = args_types of the current function
    '''
    for func in functions:
        if func["name"] == fn_name.replace('}', '').replace(',', ''):
            return func["parameters"]
    return {}


def get_response(
            llm: Small_LLM_Model, vocab: dict[str, int], words: list[int],
            allowed_parts: dict[str, set[int]], functions: list[dict],
            context: str, prompt: str
        ) -> str:
    '''
    Return the str corresponding to the llm response

    Args:
        llm: Small_LLM_Model = The LLM model used
        vocab: dict[str, int] = The available vocabulary
        allowed_parts: dict[str, set[int]] = The allowed parts
        functions: list[dict] = All the function definitions
        context: str = The encode context of the LLM
        prompt: str = The prompt the LLM will answer
    Return:
        res: str = Return of the LLM
    '''
    # set the prompt for the fn_name
    res: str = '\t{\n\t\t"prompt": "' + prompt.replace('"', "'")
    res += '",\n\t\t"name": "'
    final_prompt: str = context + res

    print(res, end="")

    # Updating res with the LLM response for the fn_name
    fn_name: str = get_fn_name(
        llm, vocab, words, final_prompt,
        [func["name"] for func in functions]
    )

    print(fn_name, end="")

    res += fn_name

    more: str = '\t\t"parameters": {'
    print(more, end="")

    res += more
    context = get_context_args(functions, fn_name[:-3])
    final_prompt = context + res

    # Update the prompt for the args
    args_types: dict[str, str] = get_args_types(functions, fn_name[:-3])
    args: str = get_args(
        llm, vocab, words, args_types, final_prompt, allowed_parts
    )

    print(args, end="")
    res += args

    end: str = '\n\t}'
    print(end, end="")
    res += end

    return res
